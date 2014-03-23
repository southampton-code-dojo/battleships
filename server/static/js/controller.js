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