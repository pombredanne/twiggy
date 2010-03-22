### some thoughts ###

import twiggy
from twiggy import log

## log is a magic object which makes loggers on attribute access ##

log.database.debug("SELECTing stuff: %d rows", len(cursor))
log.database.debug("got %(num)d things", num=len(cursor))

log.webserver.info("shutting down")

## you can test if a message would emit anything - this construct should be discouraged tho
if log.database.would_emit(twiggy.INFO):
    do_something_slow() 

## if we're running interactively, there's a preconfigured logger that prints to the terminal.  Master logger is silent. ##

log.shell.warning("OMG Snakes!", supress_newlines=False)

## tracebacks are available
log.database.error("Something went wrong!", error_traceback=True)
log.database.info("Just letting you know what's up", always_traceback=True)

## The magic log cannot be used directly.  Any non-level name is valid.
log.error("Pants on fire") ==> raises AttributeError

## Log names can be dotted to arbitrary # of levels (perhaps capped?)
log.myapp.somelib.warning("Woot") ==> WARNING myapp.somelib Woot

## That all works like so: ##

log.mylogger ==> <TopLogger(name='mylogger')>
log.mylogger.configure(level = twiggy.INFO, list_of_emitters, forward_to_master=True)

## alternately
log.mylogger.emitters = [ list_of_emitters ]
log.mylogger.forward_to_master = True/False
log.mylogger.level = twiggy.INFO

## 2nd+ level
log.mylogger.second ==> <DottedLogger(name='mylogger.second')>
log.mylogger.second.level = twiggy.DISABLED

## all other attrs (besides actual logging) raise errors - ie no emitters here
log.mylogger.second.configure(..) ==> AttributeError

### master logger ###
import twiggy

twiggy.master ==> <Logger> # same api as toplevel but no name/subs, maybe a common base class

## messages from top-level loggers may be fwd'd here

### Emitters ###
emitter = MyEmitter(level="info", format = twiggy.default_format, ...) # format is a func

if msg.level > emitter.level:
    formatted_msg = emitter.format(msg)
    emitter.emit(formatted_msg)

### Message Object ###
class Message(object):

def __init__(self, format_string, args, kwargs, text_traceback, suppress_newlines):
    self.format_strings = [..]
    self.all_args = [..]
    self.all_kwargs = [..]

### Cloning ###
# All new loggers start out as clones of twiggy.default_logger
# XXX this needs more thought

twiggy.default_logger = TopLogger?(..).bind("%(date)sT%(time)s:%(logname)s:%(next)s", date=get_date, time=get_time)

bound1 = log.webapp.bind("Request_id: %d %(next)s", 42)
bound2 = bound1.bind("Remote IP: %(ip)s %(next)s", '1.2.3.4')
bound2.info("I wear pants")

## we'll get a log message like
2010-03-17T11:48:39:webapp:Request_id: 42 Remote IP: 1.2.3.4 I wear pants

## the emitter will see a Message like
msg.format_strings =["Request_id: %d", "Remote IP: %(ip)s", "I wear pants"]
msg.all_args = [(42,), ('1.2.3.4',), ())
msg.all_kwargs = [ {}, {}, {} ]