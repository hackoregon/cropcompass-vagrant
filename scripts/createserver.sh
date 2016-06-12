#!/bin/bash

set -e

## simple error handler
error(){ echo ${1};exit 1; }

## fail if no environment is provided
#[ -z ${1} ] && error "Please provide an availability zone name (eg, us-east-1c)"

#az=$1
stack_name="CropCompassServer"

## skip stack creation if stack already exists
stack_status=$(aws cloudformation list-stacks --output text --query 'StackSummaries[?StackName==`${stack_name}`]' --query 'StackSummaries[?StackStatus==`CREATE_COMPLETE`]')
if [ -n "$stack_status" ]; then
 echo "Stack '$stack_name' already created. Skipping ..."
  exit 0
fi

#echo "Creating stack '$stack_name' in availability zone '$az'..." 2>&1

# TODO
# - template needs to accept new parameters: eg region, CIDRs, ...?

aws cloudformation create-stack \
  --stack-name $stack_name \
  --template-body "file://cropcompass.json" \
  --disable-rollback \
  --capabilities CAPABILITY_IAM

stack_creation_status="$(bash wait-for-cfn-stack-creation.sh $stack_name)"
if [ $? -ne 0 ]; then
  echo "Error: stack '$stack_name' ($stack_creation_status) failed to create properly" >&2
  exit 1
fi
