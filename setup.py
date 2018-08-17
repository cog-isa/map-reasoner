from distutils.core import setup

# with open('requirements.txt') as f:
#     required = f.read().splitlines()

setup(
    name='mapReasoner',
    version='1.0.0',
    packages=['mapreasoner'],
    package_dir={'mapreasoner': 'src'},
    #url='http://cog-isa.github.io/mapplanner/',
    license='',
    author='Alexey Kovalev',
    author_email='alexeykkov@gmail.com',
    #long_description=open('README.md').read(),
    #install_requires=required
)