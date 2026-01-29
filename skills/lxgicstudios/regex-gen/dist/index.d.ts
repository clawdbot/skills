export interface RegexResult {
    pattern: string;
    flags: string;
    explanation: string;
    examples: string[];
}
export declare function generateRegex(description: string): Promise<RegexResult>;
