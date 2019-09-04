# How to package and upload the lambda function code and dependencies?

This workshop includes the Lambda function needed to handle your skill request. The code requires some python dependencies to be included as part of your Lambda package. The dependencies are already packaged in the original function.zip.

After editing your code you will need to perform two additional steps to include your updated code in the zip file (from the ```sendSMSSkillLambda``` folder):

1. Add the lambda function code to function.zip. Use the following command:

   ```zip -g function.zip lambda_function.py```

2. **Optional - after creating initial function** Upload function.zip package to the lambda service using AWS CLI (you can upload your code using the AWS Console as well). Use the following command: (don't forget to replace ***\<your-function-name\>***)

   ```aws lambda update-function-code --function-name ***\<your-function-name\>*** --zip-file fileb://function.zip```
