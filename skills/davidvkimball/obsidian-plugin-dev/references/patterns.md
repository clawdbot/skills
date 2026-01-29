# Common Obsidian Plugin Patterns

## Table of Contents
- [Commands](#commands)
- [Ribbon Icons](#ribbon-icons)
- [Modals](#modals)
- [Events & Lifecycle](#events--lifecycle)
- [File Operations](#file-operations)
- [Editor Manipulation](#editor-manipulation)
- [Status Bar](#status-bar)
- [Context Menus](#context-menus)
- [Views](#views)

## Commands

### Simple Command

```typescript
this.addCommand({
  id: 'do-something',
  name: 'Do something',
  callback: () => {
    new Notice('Command executed!');
  }
});
```

### Editor Command

Only available when an editor is active:

```typescript
this.addCommand({
  id: 'insert-text',
  name: 'Insert text at cursor',
  editorCallback: (editor: Editor, view: MarkdownView) => {
    editor.replaceSelection('Inserted text');
  }
});
```

### Check Command

Conditionally available based on app state:

```typescript
this.addCommand({
  id: 'process-file',
  name: 'Process current file',
  checkCallback: (checking: boolean) => {
    const file = this.app.workspace.getActiveFile();
    if (file?.extension === 'md') {
      if (!checking) {
        // Execute the command
        this.processFile(file);
      }
      return true; // Command is available
    }
    return false; // Command not available
  }
});
```

### Hotkey Defaults

```typescript
this.addCommand({
  id: 'quick-action',
  name: 'Quick action',
  hotkeys: [{ modifiers: ['Mod', 'Shift'], key: 'p' }],
  callback: () => { /* ... */ }
});
```

## Ribbon Icons

```typescript
// Add ribbon icon (left sidebar)
const ribbonEl = this.addRibbonIcon('dice', 'My Plugin', (evt: MouseEvent) => {
  new Notice('Ribbon clicked!');
});

// Add CSS class for styling
ribbonEl.addClass('my-plugin-ribbon');

// Remove ribbon on unload (automatic if using this.addRibbonIcon)
```

Available icons: Use any [Lucide](https://lucide.dev/icons/) icon name.

## Modals

### Basic Modal

```typescript
import { App, Modal } from 'obsidian';

class MyModal extends Modal {
  result: string;
  onSubmit: (result: string) => void;

  constructor(app: App, onSubmit: (result: string) => void) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: 'Enter a value' });

    const inputEl = contentEl.createEl('input', { type: 'text' });
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        this.result = inputEl.value;
        this.close();
        this.onSubmit(this.result);
      }
    });

    const buttonEl = contentEl.createEl('button', { text: 'Submit' });
    buttonEl.addEventListener('click', () => {
      this.result = inputEl.value;
      this.close();
      this.onSubmit(this.result);
    });
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

// Usage
new MyModal(this.app, (result) => {
  new Notice(`You entered: ${result}`);
}).open();
```

### Confirmation Modal

```typescript
import { App, Modal, Setting } from 'obsidian';

class ConfirmModal extends Modal {
  constructor(
    app: App,
    private message: string,
    private onConfirm: () => void
  ) {
    super(app);
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('p', { text: this.message });

    new Setting(contentEl)
      .addButton(btn => btn
        .setButtonText('Cancel')
        .onClick(() => this.close()))
      .addButton(btn => btn
        .setButtonText('Confirm')
        .setWarning()
        .onClick(() => {
          this.close();
          this.onConfirm();
        }));
  }

  onClose() {
    this.contentEl.empty();
  }
}
```

## Events & Lifecycle

### File Events

```typescript
// File created
this.registerEvent(
  this.app.vault.on('create', (file) => {
    if (file instanceof TFile) {
      console.log('File created:', file.path);
    }
  })
);

// File modified
this.registerEvent(
  this.app.vault.on('modify', (file) => {
    if (file instanceof TFile) {
      console.log('File modified:', file.path);
    }
  })
);

// File deleted
this.registerEvent(
  this.app.vault.on('delete', (file) => {
    console.log('File deleted:', file.path);
  })
);

// File renamed
this.registerEvent(
  this.app.vault.on('rename', (file, oldPath) => {
    console.log(`Renamed: ${oldPath} -> ${file.path}`);
  })
);
```

### Layout Events

```typescript
// Active file changed
this.registerEvent(
  this.app.workspace.on('active-leaf-change', (leaf) => {
    const file = this.app.workspace.getActiveFile();
    if (file) {
      console.log('Active file:', file.path);
    }
  })
);

// Layout changed
this.registerEvent(
  this.app.workspace.on('layout-change', () => {
    console.log('Layout changed');
  })
);
```

### Intervals

```typescript
// Auto-cleared on plugin unload
this.registerInterval(
  window.setInterval(() => {
    console.log('Periodic task');
  }, 60000) // Every minute
);
```

### DOM Events

```typescript
// Auto-removed on plugin unload
this.registerDomEvent(document, 'click', (evt: MouseEvent) => {
  console.log('Document clicked');
});
```

## File Operations

### Read File

```typescript
const file = this.app.vault.getAbstractFileByPath('path/to/file.md');
if (file instanceof TFile) {
  const content = await this.app.vault.read(file);
  // or cached read (faster, may be stale)
  const cachedContent = await this.app.vault.cachedRead(file);
}
```

### Write File

```typescript
const file = this.app.vault.getAbstractFileByPath('path/to/file.md');
if (file instanceof TFile) {
  await this.app.vault.modify(file, 'New content');
}
```

### Create File

```typescript
// Create with content
const newFile = await this.app.vault.create('path/to/new.md', 'Initial content');

// Create folder if needed
await this.app.vault.createFolder('path/to/folder');
```

### Delete File

```typescript
const file = this.app.vault.getAbstractFileByPath('path/to/file.md');
if (file instanceof TFile) {
  await this.app.vault.delete(file);
  // or move to trash
  await this.app.vault.trash(file, true);
}
```

### Get All Files

```typescript
const markdownFiles = this.app.vault.getMarkdownFiles();
const allFiles = this.app.vault.getFiles();
```

## Editor Manipulation

### Get/Set Selection

```typescript
editorCallback: (editor: Editor) => {
  // Get selection
  const selection = editor.getSelection();
  
  // Replace selection
  editor.replaceSelection('new text');
  
  // Get cursor position
  const cursor = editor.getCursor();
  
  // Set cursor position
  editor.setCursor({ line: 0, ch: 0 });
  
  // Get line content
  const line = editor.getLine(cursor.line);
  
  // Replace range
  editor.replaceRange('text', 
    { line: 0, ch: 0 }, 
    { line: 0, ch: 5 }
  );
}
```

### Get Full Document

```typescript
editorCallback: (editor: Editor) => {
  const content = editor.getValue();
  editor.setValue('Completely new content');
}
```

## Status Bar

```typescript
// Add status bar item
const statusBarEl = this.addStatusBarItem();
statusBarEl.setText('Status: Ready');

// Update later
statusBarEl.setText('Status: Processing...');

// Note: Status bar not available on mobile
```

## Context Menus

### File Menu

```typescript
this.registerEvent(
  this.app.workspace.on('file-menu', (menu, file) => {
    menu.addItem((item) => {
      item
        .setTitle('My action')
        .setIcon('star')
        .onClick(() => {
          new Notice(`Action on ${file.path}`);
        });
    });
  })
);
```

### Editor Menu

```typescript
this.registerEvent(
  this.app.workspace.on('editor-menu', (menu, editor, view) => {
    menu.addItem((item) => {
      item
        .setTitle('Process selection')
        .setIcon('wand')
        .onClick(() => {
          const selection = editor.getSelection();
          // Process selection
        });
    });
  })
);
```

## Views

### Custom View

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';

const VIEW_TYPE = 'my-custom-view';

class MyView extends ItemView {
  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType(): string {
    return VIEW_TYPE;
  }

  getDisplayText(): string {
    return 'My View';
  }

  getIcon(): string {
    return 'star';
  }

  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.createEl('h2', { text: 'My Custom View' });
  }

  async onClose() {
    // Cleanup
  }
}

// Register in plugin
this.registerView(VIEW_TYPE, (leaf) => new MyView(leaf));

// Open the view
this.app.workspace.getRightLeaf(false)?.setViewState({
  type: VIEW_TYPE,
  active: true,
});
```

### Activate Existing View

```typescript
async activateView() {
  const { workspace } = this.app;
  
  let leaf = workspace.getLeavesOfType(VIEW_TYPE)[0];
  
  if (!leaf) {
    const rightLeaf = workspace.getRightLeaf(false);
    if (rightLeaf) {
      await rightLeaf.setViewState({ type: VIEW_TYPE, active: true });
      leaf = rightLeaf;
    }
  }
  
  if (leaf) {
    workspace.revealLeaf(leaf);
  }
}
```
