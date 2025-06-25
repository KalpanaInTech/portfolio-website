import json
import boto3
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCounter')

# Custom function to convert Decimal to int or float
def decimal_to_int(d):
    if isinstance(d, Decimal):
        return int(d)  # You can use float(d) if decimals are needed
    raise TypeError

def lambda_handler(event, context):
    try:
        # Fetch current visitor count
        response = table.get_item(Key={'id': 'visitors'})
        
        # Check if the item exists
        if 'Item' in response:
            # If it exists, fetch the count
            count = response['Item']['count']
        else:
            # If it doesn't exist, set the count to 0
            count = 0

        # Increment the count
        count += 1
        
        # Update the count in DynamoDB using ExpressionAttributeNames for reserved words
        table.update_item(
            Key={'id': 'visitors'},
            UpdateExpression='SET #cnt = :val',
            ExpressionAttributeNames={
                '#cnt': 'count'  # Alias for the reserved word 'count'
            },
            ExpressionAttributeValues={':val': count}
        )

        # Convert the count from Decimal to a regular number (int)
        count = decimal_to_int(count)

        # Return the correct response format
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Allow CORS
            },
            'body': json.dumps({'visitor_count': count})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
