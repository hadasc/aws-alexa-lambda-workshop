# Part 2 - Email dictation skill

For this part we are going to use the basic skill we have created in [Part 1 - Create your first skill](BuildYourFirstSkill.md). If you did not complete this part, please do it now and come back to part 2 later.

## Extending our current skills
As mentioned before, we will use the exiting skill and intents you should have from step 1.

For email dictation, we will need to extend the basic ```GetMyName``` intent to deal with multiple Utterances, Slots and additional components (such as our backend endpoint to process the email).

### Rename your intent
As a first step, let's rename the intent to ```SendEmail```. Click on the intent name and change it. Save your model to apply changes.

### Adding additional slots
Our email skill will need several slots to send our email:
- Sender name - We will use the already available ```myName``` slot.
- Recipient name (```toName```)
- Recipient email (```toEmail```)
- Email subject (```subject```)
- Email body (```body```)

Go and add the missing slots and define slot types, prompts and user utterances.

At the end of the process you should have something like the next screenshot in your Intent Slots list:
![Intent Slots](screenshots/Screen5.png)

The ```AMAZON.SearchQuery``` slot type is used for open text inputs in our skill.

Ready to move on? [Click here - Part 3 >>](AddTranslation.md)
