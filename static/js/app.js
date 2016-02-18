app = angular.module("lights-app", []);

app.controller("LightsController", function($http) {
    var self = this;
    self.lights = "LIGHTS";
    self.triggers = [];
    self.newTrigger = new Trigger();

    self.toggle = function() {
        $http.get("/api/toggle").success(function(data) {
            self.updateState();
        });
    };

    self.setState = function(state) {
        $http.put("/api/state", {state: state}).success(function(data) {
            self.updateState();
        })
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
            self.updateTriggers();
        });
    };

    self.removeTrigger = function(jobId) {
        $http.delete("api/triggers/" + jobId).success(function(data) {
            self.updateTriggers();
        });
    };

    self.updateState();
    self.updateTriggers();

    return self;
});
