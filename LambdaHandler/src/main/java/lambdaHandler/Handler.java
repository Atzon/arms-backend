package lambdaHandler;

import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.PutItemOutcome;
import com.amazonaws.services.dynamodbv2.document.spec.PutItemSpec;
import com.amazonaws.services.dynamodbv2.model.ConditionalCheckFailedException;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import messageFormat.ErrorMessage;
import messageFormat.Message;

public class Handler implements RequestHandler<Message, String> {

    private DynamoDB dynamoDb;
    private String DYNAMODB_TABLE_NAME = "Points";
    private Regions REGION = Regions.US_EAST_1;

    public String handleRequest(Message message, Context context) {

        LambdaLogger logger = context.getLogger();
        this.initDynamoDbClient();
        ErrorMessage returnMessage = message.validate();
        if(returnMessage == null){
            persistData(message);
            logger.log("Added to database successfully.");
            return String.format("Success");

        }
        logger.log("Problem with your message: "+returnMessage);
        return String.format("[ERROR]  %s.", returnMessage);
    }

    private PutItemOutcome persistData(Message message)
            throws ConditionalCheckFailedException {
        return this.dynamoDb.getTable(DYNAMODB_TABLE_NAME)
                .putItem(
                        new PutItemSpec().withItem(new Item()
                                .withString("DeviceName", message.getDeviceName())
                                .withString("DateTime", message.getDatetime())
                                .withDouble("Latitude", message.getLatitude())
                                .withDouble("Longitude", message.getLongitude())
                                .withDouble("PM2_5", message.getPm2_5())
                                .withDouble("PM10", message.getPm10())));
    }

    private void initDynamoDbClient() {
        AmazonDynamoDBClient client = new AmazonDynamoDBClient();
        client.setRegion(Region.getRegion(REGION));
        this.dynamoDb = new DynamoDB(client);
    }
}