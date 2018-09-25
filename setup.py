from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='text2num',
      version='1.0',
      description='Parse and convert numbers written in french into their digit representation.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Filters',
        'Natural Language :: French'
      ],
      keywords='french NLP words-to-numbers',
      url='https://github.com/allo-media/text2num',
      author='Allo-Media',
      author_email='contact@allo-media.fr',
      license='MIT',
      packages=find_packages(),
      # install_requires=[
      #     'markdown',
      # ],
      test_suite='text_to_num.tests',
      include_package_data=True,
      zip_safe=False)