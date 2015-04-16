<!doctype html>
<html class="no-js" lang="en" ng-app="battleships">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Battleships</title>
    <link rel="stylesheet" href="static/css/app.css" />
    <script src="static/bower_components/modernizr/modernizr.js"></script>
</head>
<body>
    <div class="row">
        <div class="large-12 columns">
            <h1>Battleships</h1>

            <h2>Leaderboard</h2>
            <table style="width: 100%;" ng-controller="ScoreListCtrl as score">
                <thead>
                    <tr>
                        <th>Entry</th>
                        <th style="width: 50%">Score</th>
                    </tr>
                </thead>
                <tbody>
                    <tr ng-repeat="entry in entries|orderBy:winPercentage">
                        <td>{{entry.name}}</td>
                        <td>
                            <div class="progress">
                                <span class="meter" style="width: {{(entry.wins/(entry.losses+entry.wins)) * 100}}%; background: {{entry|bgcolour}};"></span>
                                <span class="progress-text">{{entry.wins}} Wins, {{entry.losses}} Losses</span>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="row">
        <div class="large-12 columns">
            <div class="panel">
                <h2>How to play</h2>
                <p>1. Ensure you have python2, pip, and virtualenv installed.</p>
                <p>2. Update config to match the live server address.</p>
                <code>nano config</code>
                <p>3. Run the setup script.</p>
                <code>./setup</code>
                <p>4. Run a local server.</p>
                <code>./run-server</code>
                <p>5. Open your server's webpage.</p>
                <code>open http://localhost:8080</code>
                <p>6. Make a copy of the demo code</p>
                <code>cp demo.py myentry.py</code>
                <p>7. Update the TEAM_NAME variable in your entry. It should be something unique.</p>
                <p>8. Modify you entry until it works as you like. Testing the entry by submitting it to your local server.</p>
                <code>./submit myentry.py</code>
                <p>9. When you're ready, submit your entry to the live server.</p>
                <code>./submit live myentry.py</code>
                <p>You can resubmit as many times as you like and your entry will compete with all other entries submitted. Once everyone has finished the scores will be cleared and every entry will play every other entry.</p>
                <p>We recommend you write unit tests for your AI (example in <code>demo_tests.py</code>, run with <code>./run-tests</code>) but since you won't - change <code>config</code> and set GAMES_TO_RUN to 1 and OVERRIDE to 1. This will allow you to re-submit your AI to the local server and have it play only a single game. This will make it easier to parse your print statements/etc.</p>
            </div>
        </div>
    </div>
    
    <script src="static/bower_components/angular/angular.min.js"></script>
    <script src="static/bower_components/angular-resource/angular-resource.min.js"></script>
    <script src="static/js/controller.js"></script>
</body>
</html>
