/**
 * Angular
 */

angular.module("demoApp", ['ui.bootstrap'])
    .controller('demoCtrl', function ($scope, $modal, $log, $interval) {
        $scope.hello = "蛤蛤";

        // About Modal
            // alert settings
        $scope.alterTip = true;
        $scope.open = function (size) {

            var modalInstance = $modal.open({
                templateUrl: 'modal.html',
                controller: 'ModalInstanceCtrl',
                size: size
            });
        };
        $interval(function () {
            console.log("hello!");
        }, 50000, 0);
    });


angular.module('demoApp').controller('ModalInstanceCtrl', function ($scope, $modalInstance) {

    $scope.ok = function () {
        $modalInstance.close();
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

$(document).ready(function() {
    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    });
}
);