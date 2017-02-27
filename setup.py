try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires=[

]

testpkgs = [
    "nose==1.3.7",
    "WebTest==2.0.21",
    "coverage==4.0.3"
]
setup(description='ContactHub SDK Python',
      author='Axant',
      url='https://github.com/axant/contacthub-sdk-python',
      version='0.1',
      install_requires=install_requires,
      packages=['contacthub'],
      extras_require={
          'testing': testpkgs,
          'documentation': ['Sphinx==1.4.1']
      },
      scripts=[],
      name='contacthub',
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=testpkgs,
      )
