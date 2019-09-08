"""Send SMS app."""
import boto3
from botocore.exceptions import ClientError

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value, get_slot
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# =========================================================================================================================================
# Alexa messages
# =========================================================================================================================================
SKILL_NAME = "SMS Sender"
SMS_SENT_MESSAGE = "Your SMS was sent successfully!"
HELP_MESSAGE = "You can say alexa can you send SMS for me, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "I'm sorry, I can't help you with that.  I can send SMS for you. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."


# =========================================================================================================================================
# Skill backend implementation:
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Amazon SNS client
sns = boto3.client('sns')


# Built-in Intent Handlers
class SendNewSMSHandler(AbstractRequestHandler):
    """Handler for Skill Launch and SendSMS Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("SendSMS")(handler_input))

    def send_sms(self, handler_input):
        # Try to send the SMS.
        try:
            logger.info("In send_sms")

            RECIPIENT = get_slot_value(handler_input=handler_input, slot_name="toPhone")
            BODY_TEXT = get_slot_value(handler_input=handler_input, slot_name="body")
            FRON_NAME = get_slot_value(handler_input=handler_input, slot_name="myName")
            TO_NAME = get_slot_value(handler_input=handler_input, slot_name="toName")

            translate_slot = get_slot(handler_input=handler_input, slot_name="translate")

            #Provide the contents of the SMS.
            sms_setup = sns.set_sms_attributes(
                attributes={
                    'DefaultSenderID': FRON_NAME
                }
            )

            #Publish the SMS
       response = sns.publish(
    PhoneNumber=RECIPIENT,
    Message=body,
    Subject="winning sms",
    MessageAttributes={
        'string': {
            'DataType': 'string',
            'StringValue': 'string',
            'BinaryValue': b'bytes'
        }
    }
)

        # Display an error if something goes wrong.
        except ClientError as e:
            logger.info("SMS wasn't sent correctly!")
            logger.error(e.response['Error']['Message'])
            return False
        else:
            logger.info("SMS sent! Message ID:"),
            logger.info(response['MessageId'])
            return True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SendNewSMSlHandler")

        sms = self.send_sms(handler_input)

        if not sms:
            raise ValueError('Erorr sending SMS')
        else:
            speech = SMS_SENT_MESSAGE

            handler_input.response_builder.speak(speech).set_card(
                SimpleCard(SKILL_NAME, get_slot_value(handler_input=handler_input, slot_name="body")))
            return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(
            SimpleCard(SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak('%s (%s)' % (EXCEPTION_MESSAGE, exception)).ask(
            '%s (%s)' % (HELP_REPROMPT, exception))

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(SendNewSMSHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(LaunchRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())


# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
