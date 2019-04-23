## Nettacker Wrapper

The goal of this repo is a proof of concept for some aspects of a Capstone Project I am working on.

Goals:
1. Containerizing Nettacker with custom Dockerfile
2. Build an abstract Tool class
3. Build a Nettacker class that extends the Tool class
4. Successfully scan my raspberry Pi from python from docker from nettacker.
5. ??
6. Profit

**note:** In every terminate test, the thread that the tool is running on will eventually fail. But the tests will continue running unaffected. So when you run the tests you will see a message "exception raised in thread-10, file not found". This is not a problem as far as I can tell. 

Just be aware that when you use the terminate command it will:
	- kill whatever subprocess is running ( the tool )
	- stop the docker container
	- delete the docker container
But it does not stop the threads execution. Maybe theres a way to do that, I will look into it when we get there, but for the time being terminating an executing tool is out of scope.

Here are some sparkles for your troubles :sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles::sparkles:

Thank you
