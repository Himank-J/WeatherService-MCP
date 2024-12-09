import json
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",
    args=["server.py"], 
    env=None
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("client-weather-app")

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize the connection
            await session.initialize()
            logger.info('Connection initialised')
            logger.info('-------------')

            # List available resources
            logger.info('Listing resources:')
            resources = await session.list_resources()
            logger.info(f'Resource object looks like - {resources}')
            logger.info('-------------')

            uri = resources.resources[0].uri
            name = resources.resources[0].name
            description = resources.resources[0].description
            logger.info(f'Resource URI - {uri}')
            logger.info(f'Resource Name - {name}')
            logger.info(f'Resource Description - {description}')
            logger.info('-------------')

            # Read a resource
            logger.info(f'Reading resource: {name}')
            resource = await session.read_resource(uri)
            contents = resource.contents[0]
            weather_data = json.loads(contents.text)
            logger.info('Weather conditions are as follows:')
            logger.info(weather_data)
            logger.info('-------------')

            # List available tools
            logger.info(f'Listing tools:')
            tools = await session.list_tools()
            contents = tools.tools[0]
            tool_name = contents.name
            tool_description = contents.description
            tool_input_schema = contents.inputSchema
            logger.info(f'Tool Name - {tool_name}')
            logger.info(f'Tool Description - {tool_description}')
            logger.info(f'Tool Input schema - {tool_input_schema}')
            logger.info('-------------')
            
            # Call a tool
            result = await session.call_tool(tool_name, arguments={"city": "pune"})
            response = json.loads(result.content[0].text)
            logger.info('Forecast conditions are as follows:')
            logger.info(response)
            logger.info('-------------')

if __name__ == "__main__":
    import asyncio
    logger.info('Listening to server...')
    asyncio.run(run())