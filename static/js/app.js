app = angular.module("lights-app", []);

app.controller("LightsController", function($http) {
    var self = this;
    self.lights = "LIGHTS";
    self.message = "";
    self.triggers = [];
    self.history = [];
    self.newTrigger = new Trigger();

    self.toggle = function() {
        $http.get("/api/toggle").success(self.updateAll);
    };

    self.setState = function(state) {
        $http.put("/api/state", {state: state}).success(self.updateAll);
    };

    self.updateState = function() {
        $http.get("api/state").success(function(data) {
            self.lights = data["state"];
        });
    };

    self.updateTriggers = function() {
        $http.get("api/triggers").success(function(data) {
            self.triggers = data.map(function(data) {
                return new Trigger(data);
            });
            self.triggers.sort(function(a, b) {
                return a.next_run_time - b.next_run_time;
            })
        });
    };

    self.addTrigger = function() {
        $http.put("api/triggers", self.newTrigger.asData()).success(function(data) {
            self.newTrigger = new Trigger();
            self.updateAll();
        });
    };

    self.removeTrigger = function(jobId) {
        $http.delete("api/triggers/" + jobId).success(self.updateAll);
    };

    self.updateHistory = function() {
        $http.get("api/history").success(function(data) {
            self.history = data.map(function(data) {
                return new Entry(data);
            });
            self.history.sort(function(a, b) {
                return b.timestamp - a.timestamp;
            });
        })
    };

    self.stop = function() {
        $http.get("api/stop").success(function(data) {
            self.message = "Stopped " + data["stop"];
        })
    };

    self.updateAll = function() {
        self.updateState();
        self.updateTriggers();
        self.updateHistory();
    };

    self.updateAll();


    return self;
});
