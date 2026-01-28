export interface SecretFinding {
    file: string;
    line: number;
    type: string;
    severity: string;
    snippet: string;
}
export declare function scanFile(filePath: string): Promise<SecretFinding[]>;
export declare function scanDirectory(dir: string): Promise<SecretFinding[]>;
export declare function aiAnalyze(findings: SecretFinding[]): Promise<string>;
