from bs4 import BeautifulSoup

file = open('config.xml')
soup = BeautifulSoup(file, 'lxml')

project = soup.find('project')
git_config = soup.find('hudson.plugins.git.userremoteconfig')
label = soup.find('assignedname')
artifact = soup.find('hudson.tasks.artifactarchiver')
junit = soup.find('hudson.tasks.junit.junitresultarchiver')

if not project: 
    exit("Not a freestyle project")

builders = soup.find('builders')



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
        return "timeout(time:" + obj.timeoutminutes.text + ", unit: 'MINUTES') {\n" + shell_step(obj) + "\n}" 
    
    # -------------------------

    # connect the xml tags to the appropriate function to render the step
    builder_converters = {    
        'hudson.tasks.shell' : shell_step,
        'hudson.tasks.batchfile' : bat_step,
        'hudson.plugins.build__timeout.buildstepwithtimeout' : timeout_step
    }
    
    steps = []
    for builder in builders:     
        if builder.name and builder.name in builder_converters:                         
            method = builder_converters[builder.name]            
            steps.append(method(builder))
    return steps
        
    
step_listing = assemble_steps(builders)        
    
       
        
print """
package {

    


}    
"""
            
print step_listing[2]
