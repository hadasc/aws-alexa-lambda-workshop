# How to package and upload the lambda function code and dependencies?

The dependencies are already packaged in function.zip.

Therefore there are two additional steps that are needed:

1. Add the lambda function code to function.zip. Use the following command:

   zip -g function.zip lambda_function.py
   
2. Upload function.zip package to the lambda service. Use the following command: (don't forget to replace ***\<your-function-name\>***)

   aws lambda update-function-code --function-name ***\<your-function-name\>*** --zip-file fileb://function.zip
