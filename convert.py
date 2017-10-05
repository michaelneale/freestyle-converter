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

def shelly(script):
    return "yeah sh"

def bat(script):
    return "yeah bat"

def timeout(obj):
    return "timey"

builder_converters = {    
    'hudson.tasks.shell' : shelly,
    'hudson.tasks.batchfile' : bat,
    'hudson.plugins.build__timeout.buildstepwithtimeout' : timeout
}

steps = []

for builder in builders:     
    if builder.name and builder.name in builder_converters:                         
        method = builder_converters[builder.name]
        steps.append(method(builder))
        
print steps
