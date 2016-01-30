app = angular.module("lights-app", []);

app.controller("LightsController", function($http) {
    var self = this;
    self.lights = "LIGHTS";

    self.toggle = function() {
        $http.get("/api/toggle").success(function(data) {
            self.getLights();
        });
    };

    self.setLights = function(state) {
        $http.put("/api/lights", {lights: state}).success(function(data) {
            self.getLights();
        })
    };

    self.getLights = function() {
        $http.get("api/lights").success(function(data) {
            self.lights = data["light"];
        });
    };

    self.getLights();

    return self;
});