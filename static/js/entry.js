function Entry(input) {
    this.datetime = moment(input.timestamp * 1000).toDate();
    this.timestamp = input.timestamp;
    this.state = input.state === "True";
    this.source = input.source;
}