# Reptile Framework

## What is it?

Reptile Framework (RepFW) is a 100% Python test automation framework
(like PyUnit) with a special feature of 100% Robot Framework compatible log
(XML) output.

It is intended as a replacement or addition to Robot Framework based testing,
especially for those cases where it's the developers that are writing the test
cases.

## Current status

Current development status is early Proof of Concept. RepFW is not yet ready
for production. I'm looking for volunteers to test RepFW in small test projects
to get some feedback on the structure and API of RepFW and to get some ideas
for further development.

## Installation

Clone the sources.

You will also need Robot Framework to be installed. RepFW is using the XML
output logger of Robot Framework in order to generate the XML log file. Also,
rebot command of Robot Framework will be needed in order to convert the XML log
files into HTML log files.

## Running the PoC

First, run the PoC SUT (Software Under testing) in one terminal:

./gameserver.py

Then, in an another terminal, run the test suite:

./reptileframework.py  ./testgameserver.py

To get HTML log and report, run:

rebot out.xml

## Writing test suites, test cases and keywords

Reptile framework expects to get a test module, i.e. a python source file, as
command-line argument. The test module is expected to contain a factory function
called test_factory(). When called, this function is expected to return a Python
class object that represents a single test suite.

Within test suite object, there can be any number of functions starting with
name "test" and decorated with @testcase. These functions represent test cases
within that suite.

Anywhere upon call chain of the test cases, any function decorated with @keyword
gets logged.

Documentation of the test suite class and testcase/keyword functions are
propagated to the generated log files.

There are also some other decorators, see decorators.py for details.

## What is missing

A lot. Fortunately, PyUnit stuff can be used to some extent.

Tagging system exists, but is not yet tested.

In general, the framework is not properly tested yet.
