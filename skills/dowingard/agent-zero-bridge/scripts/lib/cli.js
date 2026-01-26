/**
 * CLI Argument Parser (shared utility)
 */

function parseArgs(args) {
    const result = { command: null, args: [], options: {} };
    let i = 0;
    
    while (i < args.length) {
        const arg = args[i];
        
        if (arg.startsWith('--')) {
            const key = arg.slice(2);
            const next = args[i + 1];
            
            if (key === 'new' || key === 'help' || key === 'json') {
                result.options[key] = true;
            } else if (next && !next.startsWith('--')) {
                // Handle repeated options (like --attach)
                if (result.options[key]) {
                    if (!Array.isArray(result.options[key])) {
                        result.options[key] = [result.options[key]];
                    }
                    result.options[key].push(next);
                } else {
                    result.options[key] = next;
                }
                i++;
            } else {
                result.options[key] = true;
            }
        } else if (!result.command) {
            result.command = arg;
        } else {
            result.args.push(arg);
        }
        i++;
    }
    
    return result;
}

module.exports = { parseArgs };
