/**
 * CloudAgentDelegator - Manages task delegation to cloud agents
 */
class CloudAgentDelegator {
    constructor(config = {}) {
        this.config = {
            maxRetries: config.maxRetries || 3,
            timeout: config.timeout || 30000,
            ...config
        };
        this.agents = [];
        this.agentIndexMap = new Map();
    }

    /**
     * Register a cloud agent
     * @param {Object} agent - Agent instance implementing execute method
     */
    registerAgent(agent) {
        this.agents.push(agent);
    }

    /**
     * Delegate a task to available cloud agents
     * @param {Object} task - Task object with type and data
     * @returns {Promise<Object>} Task result
     */
    async delegate(task) {
        if (this.agents.length === 0) {
            // Simulate cloud agent execution
            return this._simulateExecution(task);
        }

        const agent = this._selectAgent(task);
        return await agent.execute(task);
    }

    /**
     * Select best available agent for task
     * @private
     */
    _selectAgent(task) {
        // Filter agents by capability
        const capableAgents = this.agents.filter(agent => agent.canHandle(task));
        
        if (capableAgents.length === 0) {
            // Fallback to first available agent if none explicitly handle the task
            return this.agents[0];
        }

        // Round-robin selection among capable agents for this task type
        const taskType = task.task;
        const currentIndex = this.agentIndexMap.get(taskType) || 0;
        const agent = capableAgents[currentIndex % capableAgents.length];
        this.agentIndexMap.set(taskType, currentIndex + 1);
        return agent;
    }

    /**
     * Simulate cloud agent execution (for demonstration)
     * @private
     */
    _simulateExecution(task) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    status: 'completed',
                    task: task.task,
                    result: `Processed: ${JSON.stringify(task.data)}`,
                    timestamp: new Date().toISOString()
                });
            }, 100);
        });
    }
}

module.exports = { CloudAgentDelegator };
