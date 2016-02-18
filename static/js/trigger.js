function Trigger(input) {
    this.state = true;
    this.repeatWeekday = false;
    this.repeatWeekend = false;
    if (input !== undefined) {
        this.jobId = input.job_id;
        this.state = input.state;
        this.repeatWeekday = input.repeat_weekday;
        this.repeatWeekend = input.repeat_weekend;
        this.time = moment({hour: input.hour, minute: input.minute}).format("h:mm a");
        this.nextRunTime = moment(input.next_run_time * 1000).toDate();
    }
    this.stateName = function() {
        return this.state ? "ON" : "OFF";
    };
    this.toggleState = function() {
        this.state = !this.state;
    };
    this.toggleRepeatWeekday = function() {
        this.repeatWeekday = !this.repeatWeekday;
    };
    this.toggleRepeatWeekend = function () {
        this.repeatWeekend = !this.repeatWeekend;
    };
    this.asData = function() {
        return {
            state: this.state,
            hour: moment(this.time).hour(),
            minute: moment(this.time).minute(),
            repeat_weekday: this.repeatWeekday,
            repeat_weekend: this.repeatWeekend,
        }
    }
}