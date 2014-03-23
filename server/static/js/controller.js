// Set up an angular module for Battleships
var battleships = angular.module('battleships', ['ngResource']);

// A simple resource which can be refreshed to get the latest entries
battleships.factory('Entry', ['$resource', function($resource) {
    return $resource('entries', {});
}]);

// Controller to encapsulate the score list
battleships.controller('ScoreListCtrl', ['$scope', 'Entry', function($scope, Entry) {
    $scope.entries = Entry.query();

    $scope.winPercentage = function(entry) {
        return 0-(entry.wins/(entry.wins+entry.losses));
    };

    // Refresh the entries 10 times per second
    setInterval(function() {
        var x = Entry.query(function() {
            $scope.entries = x;
        });
    }, 100);
}]);

// Generate a colour from a string
// modified from http://stackoverflow.com/questions/3426404/
// create-a-hexadecimal-colour-based-on-a-string-with-javascript
// and http://24ways.org/2010/calculating-color-contrast/
String.prototype.getHashCode = function() {
    var hash = 0;
    if (this.length == 0) return hash;
    for (var i = 0; i < this.length; i++) {
        hash = this.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
};
Number.prototype.intToHSL = function() {
    var shortened = this % 360;
    return "hsl(" + shortened + ",100%,70%)";
};

battleships.filter('bgcolour', function() {
    return function(entry) {
        return entry.name.getHashCode().intToHSL();
    }
});