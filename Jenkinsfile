        stage 'Checkout SCM'
            checkout([
                $class: 'GitSCM',
                branches: [[name: "refs/heads/${env.BRANCH_NAME}"]],
                extensions: [[$class: 'LocalBranch']],
                userRemoteConfigs: scm.userRemoteConfigs,
                doGenerateSubmoduleConfigurations: false,
                submoduleCfg: []
            ])

        stage 'Install & Unit Tests'
            timestamps {
                timeout(time: 30, unit: 'MINUTES') {
                    try {
                        sh 'pip install -r requirements.txt'
                        sh 'python setup.py nosetests --with-xunit'
                    } finally {
                        step([$class: 'JUnitResultArchiver', testResults: 'nosetests.xml'])
                    }
                }
            }



// sh '''pip install -r requirements.txt
// cd src/
// APP_SETTINGS=config.DevelopmentConfig python -m unittest'''

