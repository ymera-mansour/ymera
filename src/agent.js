/**
 * CloudAgent - Base class for cloud agent implementations
 */
class CloudAgent {
    constructor(name, capabilities = []) {
        this.name = name;
        this.capabilities = capabilities;
        this.status = 'idle';
    }

    /**
     * Execute a delegated task
     * @param {Object} task - Task to execute
     * @returns {Promise<Object>} Execution result
     */
    async execute(task) {
        this.status = 'busy';
        
        try {
            const result = await this._process(task);
            this.status = 'idle';
            return result;
        } catch (error) {
            this.status = 'error';
            throw error;
        }
    }

    /**
     * Process the task (to be overridden by implementations)
     * @private
     */
    async _process(task) {
        return {
            status: 'completed',
            agent: this.name,
            task: task.task,
            result: task.data
        };
    }

    /**
     * Check if agent can handle task
     */
    canHandle(task) {
        return this.capabilities.includes(task.task) || this.capabilities.includes('*');
    }
}

module.exports = { CloudAgent };
