from bs4 import BeautifulSoup
from string import Template

file = open('config.xml')
soup = BeautifulSoup(file, 'lxml')

project = soup.find('project')
git_config = soup.find('hudson.plugins.git.userremoteconfig')
label = soup.find('assignednode')
artifact = soup.find('hudson.tasks.artifactarchiver')
junit = soup.find('hudson.tasks.junit.junitresultarchiver')
builders = soup.find('builders')


if not project: 
    exit("Not a freestyle project")





#
# for all the builders we find, try to find an equivalent step
#
def assemble_steps(builders):
    
    #
    # step rendering functions 
    # ------------------------
    # 
    
    def shell_step(script):
        return '\tsh \'\'\' \n\t\t' + script.command.text + '\n\t\'\'\''

    def bat_step(script):
        return '\tbat \'\'\' \n\t\t' + script.command.text + '\n\t\'\'\''

    def timeout_step(obj):        
        return "\ttimeout(time:" + obj.timeoutminutes.text + ", unit: 'MINUTES') {\n\t" + shell_step(obj).replace('\n', '\n\t') + "\n\t}" 
    
    # -------------------------

    # connect the xml tags to the appropriate function to render the step
    builder_converters = {    
        'hudson.tasks.shell' : shell_step,
        'hudson.tasks.batchfile' : bat_step,
        'hudson.plugins.build__timeout.buildstepwithtimeout' : timeout_step
    }
    
    steps = ''
    for builder in builders:     
        if builder.name and builder.name in builder_converters:                         
            method = builder_converters[builder.name]            
            steps = steps + '\n' + method(builder) + '\n'
    return steps

def render_agent(label):
    print label
    if (label): 
        return 'agent "' + label.text + '"'
    else:    
        return 'agent any'        

def render_artifact(artifact):
    if (artifact):
        return 'archive "' + artifact.artifacts.text + '"'
    else:
        return ''    

def render_junit(junit):
    if (junit):
        return 'junit "' + junit.testresults.text + '"'
    else:
        return ''
    
step_listing = assemble_steps(builders).replace('\n', '\n\t')       
    
       
template = Template("""
package {
    ${agent}
    stages {
        stage("Build") {
            steps {
                ${step_listing}
            }            
        }    
    }
    
    post {
        success {
            ${archiver}
        }
        always {
            ${junit}
        }
    }
    

}    
""")       
        
print template.substitute({'step_listing' : step_listing, 
                            'agent': render_agent(label),
                            'archiver': render_artifact(artifact),
                            'junit': render_junit(junit)})
