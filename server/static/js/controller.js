// Set up an angular module for Battleships
var battleships = angular.module('battleships', ['ngResource']);

// A simple resource which can be refreshed to get the latest entries
battleships.factory('Entry', ['$resource', function($resource) {
    return $resource('entries', {});
}]);

// Controller to encapsulate the score list
battleships.controller('ScoreListCtrl', ['$scope', 'Entry', function($scope, Entry) {
    $scope.entries = Entry.query();

    // Refresh the entries once per second
    setInterval(function() {
        $scope.entries = Entry.query();
    }, 1000);
}]);