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

print git_config
print label
#print soup.find('assignednamex')
#print soup.find('command')
builders = soup.find('builders')


builder_converters = {    
    'hudson.tasks.shell' : 'shell',
    'hudson.tasks.batchfile' : 'bat',
    'hudson.plugins.build__timeout.buildstepwithtimeout' : 'timeout'
}

for builder in builders:     
    if builder.name and builder.name in builder_converters:         
        print "----> " + builder_converters[builder.name]
