pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('lint') {
            steps {
			sh 'pylint --disable=W1202 --output-format=parseable --reports=no module > pylint.log || echo "pylint exited with $?")'
			sh 'cat render/pylint.log'

			step([
			        $class                     : 'WarningsPublisher',
			        parserConfigurations       : [[
                                              parserName: 'PYLint',
                                              pattern   : 'pylint.log'
	                                      ]],
			        unstableTotalAll           : '0',
			        usePreviousBuildAsReference: true
			])
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
		sh 'pip install -r requirements.txt'
                sh 'python setup.py install'
            }
        }
#        stage('test') {
#            steps {
#                sh 'python --version'
#            }
#        }
#        stage('upload') {
#            steps {
#                sh 'python --version'
#            }
#        }
    }
}
