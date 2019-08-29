# Alexa Lambda Workshop
In this workshop we will build an Amazon Alexa skill, backed by an [AWS Lambda](https://aws.amazon.com/lambda/), using multiple AWS services such as Amazon [SNS](https://aws.amazon.com/sns/) and [Amazon Translate](https://aws.amazon.com/translate/).

At the end of the workshop, you will have a voice skill that enables you to dictate a short message to Alexa and send it to the recipient via SMS, using [Amazon Simple Notification Service](https://aws.amazon.com/sns/), in the original language (English) or translate it to one of the 25 languages, supported by [Amazon Translate](https://aws.amazon.com/translate/).

![Architecture](screenshots/Architecture.png)

This workshop has 3 parts:

[Part 1 - Create your first skill](BuildYourFirstSkill.md)
- A basic setup of your account on Alexa Developer Console and first skill setup.

[Part 2 - SMS dictation skill](SMSDictationSkill.md)
- Extend your skill to get additional inputs from the user.
- Connect your skill to an AWS backend using AWS Lambda.

[Part 3 - Add translation capabilities to your skill](AddTranslation.md)
- Extend your skill to be able to translate your SMS based on the desired target language.

[Start Part 1 >>](BuildYourFirstSkill.md)
