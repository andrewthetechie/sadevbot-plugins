from typing import Any
from typing import Dict

from decouple import config as get_config
from errbot import arg_botcmd
from errbot import botcmd
from errbot import BotFlow
from errbot import botflow
from errbot import BotPlugin
from errbot import FLOW_END
from errbot import FlowRoot
from pendulum import parse


def get_config_item(
    key: str, config: Dict, overwrite: bool = False, **decouple_kwargs
) -> Any:
    """
    Checks config to see if key was passed in, if not gets it from the environment/config file

    If key is already in config and overwrite is not true, nothing is done. Otherwise, config var is added to config
    at key
    """
    if key not in config and not overwrite:
        config[key] = get_config(key, **decouple_kwargs)


class EventManagerPlugin(BotPlugin):
    """Manages events for SADevs"""

    def configure(self, configuration: Dict) -> None:
        """
        Configures the vlos
        """
        self.log.debug("Starting Config")
        if configuration is None:
            configuration = dict()

        # name of the channel to post in
        get_config_item("EVENT_MANAGER_TZ", configuration, default="US/Central")

        super().configure(configuration)

    @botcmd(split_args_with=None)
    def new_event(self, msg, args) -> str:
        """
        Setup a new event with sadevs. Start off with ./new event Title to your event here
        """
        msg.ctx["title"] = " ".join(args)
        return (
            "Setting up your new event. I need to know when your event is. Reply with `./new event date "
            "{date of your event}`\nYou can express your date in yyyy-mm-dd i.e. 2020-01-01"
        )

    @arg_botcmd("date", type=str)
    def new_event_date(self, msg, date: str) -> str:
        """
        Second step in setting up a new event
        """
        msg.ctx["date"] = parse(date, tz=self.config["EVENT_MANAGER_TZ"])
        return (
            "Great, got the date.\nTo continue run `./new event duration #`\n"
            "Your duration should be expressed in # of minutes, so a 1hr 30m event would be "
            "`./new event duration 90`"
        )

    @arg_botcmd("duration", type=int)
    def new_event_duration(self, msg, duration: int) -> str:
        """
        Third step in your new event.
        """
        msg.ctx["duration"] = f"{duration}m"
        return (
            "Awesome, got it!\n"
            "To continue run `./new event location {address of your event}`\n"
            "Your address should be formatted like Place Name, Street, City, State Zip.\n"
            "i.e Kimura, 152 E Pecan St #102, San Antonio, TX 78205"
        )

    @botcmd(split_args_with=None)
    def new_event_location(self, msg, args) -> str:
        """
        Fourth step in your new event
        """
        msg.ctx["location"] = " ".join(args)
        return (
            "Stored that location.\n"
            "To continue run `./new event summary {One sentenece about your event}`\n"
            "Your summary should be a short descrtiption about your event. For an example, see"
            "https://raw.githubusercontent.com/SADevs/sadevs.github.io/website/content/articles/"
            "2019_01_18_meetup_noodles.md"
        )

    @botcmd(split_args_with=None)
    def new_event_summary(self, msg, args) -> str:
        """
        Fifth step in your new event
        """
        msg.ctx["summary"] = " ".join(args)
        return (
            "Summary saved.\n"
            "To continue run `./new event description {A long form description about your event}`\n"
            "Your Description should be a couple of paragraph descrtiption about your event. For an example, see"
            "https://raw.githubusercontent.com/SADevs/sadevs.github.io/website/content/articles/"
            "2019_01_18_meetup_noodles.md"
        )

    @botcmd(split_args_with=None)
    def new_event_description(self, msg, args) -> str:
        """
        Fourth step in your new event
        """
        msg.ctx["descripton"] = " ".join(args)
        return msg.ctx


class EventManagerFlow(BotFlow):
    @botflow
    def new_event_flow(self, flow: FlowRoot):
        first_step = flow.connect("new_event")
        second_step = first_step.connect("new_event_date")
        third_step = second_step.connect("new_event_duration")
        fourth_step = third_step.connect("new_event_location")
        fifth_step = fourth_step.connect("new_event_summary")
        sixth_step = fifth_step.connect("new_event_description")
        sixth_step.connect(FLOW_END)
