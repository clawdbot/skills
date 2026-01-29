export interface CronResult {
    expression: string;
    explanation: string;
    next_runs: string[];
}
export declare function generateCron(description: string): Promise<CronResult>;
