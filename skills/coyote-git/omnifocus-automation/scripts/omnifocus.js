#!/usr/bin/env osascript -l JavaScript
/**
 * OmniFocus CLI - Omni Automation wrapper for Clawdbot
 * Usage: osascript omnifocus.js <command> [args...]
 */

function run(argv) {
  const app = Application("OmniFocus");
  const doc = app.defaultDocument;
  
  // For shell commands (needed for AppleScript workarounds)
  const currentApp = Application.currentApplication();
  currentApp.includeStandardAdditions = true;
  
  const command = argv[0];
  const args = argv.slice(1);
  
  // === HELPERS ===
  
  // Escape string for AppleScript embedded in shell
  function escapeForAppleScript(str) {
    if (!str) return '';
    // Escape backslashes first, then quotes
    return str.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
  }
  
  // Run AppleScript via shell (workaround for JXA bugs with tags/repeat)
  function runAppleScript(script) {
    // Escape for shell: single quotes with proper escaping
    const escaped = script.replace(/'/g, "'\"'\"'");
    return currentApp.doShellScript(`osascript -e '${escaped}'`);
  }
  
  function fmtDate(d) {
    if (!d) return null;
    return d.toISOString().split('T')[0];
  }
  
  function parseDate(str) {
    const d = new Date(str);
    if (isNaN(d.getTime())) throw new Error(`Invalid date: ${str}`);
    return d;
  }
  
  function findTask(id) {
    const all = doc.flattenedTasks();
    for (let i = 0; i < all.length; i++) {
      if (all[i].id() === id) return all[i];
    }
    const inbox = doc.inboxTasks();
    for (let i = 0; i < inbox.length; i++) {
      if (inbox[i].id() === id) return inbox[i];
    }
    return null;
  }
  
  function findProject(name) {
    const projects = doc.flattenedProjects();
    for (let i = 0; i < projects.length; i++) {
      if (projects[i].name() === name) return projects[i];
    }
    return null;
  }
  
  function findFolder(name) {
    const folders = doc.flattenedFolders();
    for (let i = 0; i < folders.length; i++) {
      if (folders[i].name() === name) return folders[i];
    }
    return null;
  }
  
  function findTag(name) {
    const tags = doc.flattenedTags();
    for (let i = 0; i < tags.length; i++) {
      if (tags[i].name() === name) return tags[i];
    }
    return null;
  }
  
  function getTaskTags(task) {
    try {
      const tags = task.tags();
      const result = [];
      for (let i = 0; i < tags.length; i++) {
        const name = tags[i].name();
        if (name) result.push(name);  // Filter out empty tag names
      }
      return result;
    } catch (e) {
      return [];
    }
  }
  
  function getRepeatRule(task) {
    try {
      const rule = task.repetitionRule();
      if (!rule) return null;
      // JXA returns properties directly (not as functions)
      return {
        method: rule.repetitionMethod || null,
        recurrence: rule.recurrence || null
      };
    } catch (e) {
      return null;
    }
  }
  
  function taskToObj(t) {
    return {
      id: t.id(),
      name: t.name(),
      note: t.note() || null,
      flagged: t.flagged(),
      completed: t.completed(),
      deferDate: fmtDate(t.deferDate()),
      dueDate: fmtDate(t.dueDate()),
      completionDate: fmtDate(t.completionDate()),
      project: t.containingProject() ? t.containingProject().name() : null,
      tags: getTaskTags(t),
      repeat: getRepeatRule(t)
    };
  }
  
  function err(msg) {
    return JSON.stringify({error: msg});
  }
  
  function ok(data) {
    return JSON.stringify(Object.assign({success: true}, data), null, 2);
  }
  
  // === COMMANDS ===
  
  switch (command) {
    
    // --- LIST COMMANDS ---
    
    case 'inbox': {
      const tasks = doc.inboxTasks();
      const result = [];
      for (let i = 0; i < tasks.length; i++) {
        const t = tasks[i];
        result.push({
          id: t.id(),
          name: t.name(),
          flagged: t.flagged(),
          dueDate: fmtDate(t.dueDate()),
          tags: getTaskTags(t)
        });
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'folders': {
      const folders = doc.folders();
      const result = [];
      for (let i = 0; i < folders.length; i++) {
        result.push({
          id: folders[i].id(),
          name: folders[i].name(),
          projectCount: folders[i].projects().length
        });
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'projects': {
      const folderName = args[0];
      let projects;
      if (folderName) {
        const folder = findFolder(folderName);
        if (!folder) return err(`Folder not found: ${folderName}`);
        projects = folder.projects();
      } else {
        projects = doc.flattenedProjects();
      }
      const result = [];
      for (let i = 0; i < projects.length; i++) {
        const p = projects[i];
        result.push({
          id: p.id(),
          name: p.name(),
          folder: p.folder() ? p.folder().name() : null,
          taskCount: p.tasks().length,
          status: p.status()
        });
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'tasks': {
      const projectName = args[0];
      if (!projectName) return err("Project name required");
      const project = findProject(projectName);
      if (!project) return err(`Project not found: ${projectName}`);
      const tasks = project.flattenedTasks();
      const result = [];
      for (let i = 0; i < tasks.length; i++) {
        result.push(taskToObj(tasks[i]));
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'tags': {
      const tags = doc.flattenedTags();
      const result = [];
      for (let i = 0; i < tags.length; i++) {
        result.push({
          id: tags[i].id(),
          name: tags[i].name()
        });
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'today': {
      const now = new Date();
      const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const todayEnd = new Date(todayStart.getTime() + 86400000);
      const all = doc.flattenedTasks();
      const result = [];
      for (let i = 0; i < all.length; i++) {
        const t = all[i];
        if (t.completed()) continue;
        const due = t.effectiveDueDate();
        if (due && due < todayEnd) {
          result.push(taskToObj(t));
        }
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'flagged': {
      const all = doc.flattenedTasks();
      const result = [];
      for (let i = 0; i < all.length; i++) {
        const t = all[i];
        if (!t.completed() && t.flagged()) {
          result.push(taskToObj(t));
        }
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'search': {
      const query = args.join(' ').toLowerCase();
      if (!query) return err("Search query required");
      const all = doc.flattenedTasks();
      const result = [];
      for (let i = 0; i < all.length; i++) {
        const t = all[i];
        if (t.name().toLowerCase().includes(query)) {
          result.push(taskToObj(t));
        }
      }
      return JSON.stringify(result, null, 2);
    }
    
    case 'info': {
      const taskId = args[0];
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      return JSON.stringify(taskToObj(task), null, 2);
    }
    
    // --- CREATE COMMANDS ---
    
    case 'add': {
      const name = args[0];
      const projectName = args[1];
      if (!name) return err("Task name required");
      let task;
      if (projectName) {
        const project = findProject(projectName);
        if (!project) return err(`Project not found: ${projectName}`);
        task = app.Task({name: name});
        project.tasks.push(task);
      } else {
        task = app.InboxTask({name: name});
        doc.inboxTasks.push(task);
      }
      return ok({task: {id: task.id(), name: task.name(), project: projectName || "Inbox"}});
    }
    
    case 'newproject': {
      const name = args[0];
      const folderName = args[1];
      if (!name) return err("Project name required");
      let project;
      if (folderName) {
        const folder = findFolder(folderName);
        if (!folder) return err(`Folder not found: ${folderName}`);
        project = app.Project({name: name});
        folder.projects.push(project);
      } else {
        project = app.Project({name: name});
        doc.projects.push(project);
      }
      return ok({project: {id: project.id(), name: project.name(), folder: folderName || null}});
    }
    
    case 'newfolder': {
      const name = args[0];
      if (!name) return err("Folder name required");
      const folder = app.Folder({name: name});
      doc.folders.push(folder);
      return ok({folder: {id: folder.id(), name: folder.name()}});
    }
    
    case 'newtag': {
      const name = args[0];
      if (!name) return err("Tag name required");
      let tag = findTag(name);
      if (tag) return ok({tag: {id: tag.id(), name: tag.name()}, existed: true});
      tag = app.Tag({name: name});
      doc.tags.push(tag);
      return ok({tag: {id: tag.id(), name: tag.name()}, created: true});
    }
    
    // --- MODIFY COMMANDS ---
    
    case 'complete': {
      const taskId = args[0];
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      task.markComplete();
      return ok({task: taskToObj(task)});
    }
    
    case 'uncomplete': {
      const taskId = args[0];
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      task.markIncomplete();
      return ok({task: taskToObj(task)});
    }
    
    case 'delete': {
      const taskId = args[0];
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      const name = task.name();
      app.delete(task);
      return ok({deleted: {id: taskId, name: name}});
    }
    
    case 'rename': {
      const taskId = args[0];
      const newName = args.slice(1).join(' ');
      if (!taskId || !newName) return err("Task ID and new name required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      task.name = newName;
      return ok({task: taskToObj(task)});
    }
    
    case 'note': {
      const taskId = args[0];
      const noteText = args.slice(1).join(' ');
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      const existing = task.note() || '';
      task.note = existing ? existing + '\n' + noteText : noteText;
      return ok({task: taskToObj(task)});
    }
    
    case 'setnote': {
      const taskId = args[0];
      const noteText = args.slice(1).join(' ');
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      task.note = noteText;
      return ok({task: taskToObj(task)});
    }
    
    case 'defer': {
      const taskId = args[0];
      const dateStr = args[1];
      if (!taskId || !dateStr) return err("Task ID and date required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      task.deferDate = parseDate(dateStr);
      return ok({task: taskToObj(task)});
    }
    
    case 'due': {
      const taskId = args[0];
      const dateStr = args[1];
      if (!taskId || !dateStr) return err("Task ID and date required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      task.dueDate = parseDate(dateStr);
      return ok({task: taskToObj(task)});
    }
    
    case 'flag': {
      const taskId = args[0];
      const flagValue = args[1] !== 'false';
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      task.flagged = flagValue;
      return ok({task: taskToObj(task)});
    }
    
    case 'tag': {
      // JXA has a bug with addTag, use AppleScript via shell
      const taskId = args[0];
      const tagName = args[1];
      if (!taskId || !tagName) return err("Task ID and tag name required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      
      // Use AppleScript for tagging (JXA has type conversion bugs)
      const safeTagName = escapeForAppleScript(tagName);
      const script = `
        tell application "OmniFocus"
          tell default document
            set theTask to first flattened task whose id is "${taskId}"
            try
              set theTag to first flattened tag whose name is "${safeTagName}"
            on error
              set theTag to make new tag with properties {name:"${safeTagName}"}
            end try
            add theTag to tags of theTask
          end tell
        end tell
      `;
      try {
        runAppleScript(script);
      } catch(e) {
        return err(`Failed to add tag: ${e.message}`);
      }
      
      // Refresh and return
      const updated = findTask(taskId);
      return ok({task: taskToObj(updated)});
    }
    
    case 'untag': {
      const taskId = args[0];
      const tagName = args[1];
      if (!taskId || !tagName) return err("Task ID and tag name required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      
      // Use AppleScript for untagging
      const safeTagName = escapeForAppleScript(tagName);
      const script = `
        tell application "OmniFocus"
          tell default document
            set theTask to first flattened task whose id is "${taskId}"
            set theTag to first flattened tag whose name is "${safeTagName}"
            remove theTag from tags of theTask
          end tell
        end tell
      `;
      try {
        runAppleScript(script);
      } catch(e) {
        return err(`Failed to remove tag: ${e.message}`);
      }
      
      const updated = findTask(taskId);
      return ok({task: taskToObj(updated)});
    }
    
    case 'repeat': {
      // Use AppleScript for repetition (JXA has issues)
      const taskId = args[0];
      const method = args[1] || 'fixed';
      const interval = parseInt(args[2]) || 1;
      const unit = args[3] || 'weeks';
      
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      
      // Map method for AppleScript
      const methodMap = {
        'fixed': 'fixed repetition',
        'due-after-completion': 'due after completion',
        'defer-after-completion': 'start after completion'
      };
      const asMethod = methodMap[method];
      if (!asMethod) return err(`Invalid method: ${method}. Use: fixed, due-after-completion, defer-after-completion`);
      
      // Map unit
      const unitMap = {
        'days': 'day', 'day': 'day',
        'weeks': 'week', 'week': 'week', 
        'months': 'month', 'month': 'month',
        'years': 'year', 'year': 'year'
      };
      const asUnit = unitMap[unit.toLowerCase()];
      if (!asUnit) return err(`Invalid unit: ${unit}. Use: days, weeks, months, years`);
      
      const script = `
        tell application "OmniFocus"
          tell default document
            set theTask to first flattened task whose id is "${taskId}"
            set repetition rule of theTask to {repetition method:${asMethod}, recurrence:"FREQ=${asUnit.toUpperCase()}LY;INTERVAL=${interval}"}
          end tell
        end tell
      `;
      try {
        runAppleScript(script);
      } catch(e) {
        return err(`Failed to set repeat: ${e.message}`);
      }
      
      const updated = findTask(taskId);
      return ok({task: taskToObj(updated)});
    }
    
    case 'unrepeat': {
      const taskId = args[0];
      if (!taskId) return err("Task ID required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      
      const script = `
        tell application "OmniFocus"
          tell default document
            set theTask to first flattened task whose id is "${taskId}"
            set repetition rule of theTask to missing value
          end tell
        end tell
      `;
      try {
        runAppleScript(script);
      } catch(e) {
        return err(`Failed to remove repeat: ${e.message}`);
      }
      
      const updated = findTask(taskId);
      return ok({task: taskToObj(updated)});
    }
    
    case 'move': {
      const taskId = args[0];
      const projectName = args[1];
      if (!taskId || !projectName) return err("Task ID and project name required");
      const task = findTask(taskId);
      if (!task) return err(`Task not found: ${taskId}`);
      const project = findProject(projectName);
      if (!project) return err(`Project not found: ${projectName}`);
      task.assignedContainer = project;
      return ok({task: taskToObj(task)});
    }
    
    // --- HELP ---
    
    case 'help':
    default: {
      return JSON.stringify({
        commands: {
          // List
          inbox: "List inbox tasks",
          folders: "List all folders",
          projects: "List projects [folder]",
          tasks: "List tasks in project <project>",
          tags: "List all tags",
          today: "List tasks due today or overdue",
          flagged: "List flagged tasks",
          search: "Search tasks <query>",
          info: "Get task details <taskId>",
          // Create
          add: "Add task <name> [project]",
          newproject: "Create project <name> [folder]",
          newfolder: "Create folder <name>",
          newtag: "Create tag <name>",
          // Modify
          complete: "Complete task <taskId>",
          uncomplete: "Uncomplete task <taskId>",
          delete: "Delete task <taskId>",
          rename: "Rename task <taskId> <name>",
          note: "Append to note <taskId> <text>",
          setnote: "Replace note <taskId> <text>",
          defer: "Set defer date <taskId> <date>",
          due: "Set due date <taskId> <date>",
          flag: "Set flag <taskId> [true|false]",
          tag: "Add tag <taskId> <tag>",
          untag: "Remove tag <taskId> <tag>",
          repeat: "Set repeat <taskId> <method> <interval> <unit>",
          unrepeat: "Remove repeat <taskId>",
          move: "Move task <taskId> <project>"
        }
      }, null, 2);
    }
  }
}
