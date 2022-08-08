from setuptools import setup

setup(name='timing_games_package',
      author='Weinan Gong',
      author_email='wgong4@ucsc.edu',
      version='0.1',
      description='Timing Games',
      packages=['timing_games_package'],
      zip_safe=True,
      # include_package_data=True,
      install_requires=[
          'pandas>=0.25.0',
          'numpy>=1.16.3',
          'matplotlib>=3.0.0',
      ],

      )
