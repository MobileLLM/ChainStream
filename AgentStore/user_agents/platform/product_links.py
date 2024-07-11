from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model, make_prompt


class ProductLinks(Agent):
    """
    Several steps:
    1. fetch all items from a platform's (twitter, instagram, youtube etc)
    2. distribute items to different streams based on author
    3. filter etch items containing an advertisement
    4. fetch advertisement products name, description etc. and push to advertisement product stream
    5. find products in Amazons and tag links to them

    we start from step 3.
    """

    def __init__(self):
        super().__init__("product_links")
        self.messages_stream = get_stream("messages")
        self.ad_stream = create_stream("advertisement_messages")
        self.product_stream = create_stream("advertisement_products")
        self.product_with_links_stream = create_stream("advertisement_products_with_links")

        self.llm = get_model("text")

    def start(self):
        def filter_advertisement(message):
            prompt = "Is following message an advertisement? Answer yes or no. Here is the message: "
            response = self.llm.query(prompt + message)
            if response == "yes":
                self.ad_stream.add_item(message)

        self.messages_stream.for_each(self, filter_advertisement)

        def fetch_advertisement_product(message):
            prompt = ("What is the name, description, price, etc. of the advertisement product? Answer like this: [{"
                      "name: <product_name>, description: <product_description>}].\nHere is the message:")
            response = self.llm.query(prompt + message)
            product_info = eval(response)
            for item in product_info:
                item["message"] = message
                self.product_stream.add_item(item)
        self.ad_stream.for_each(self, fetch_advertisement_product)

        def find_links_to_products(product):
            pass
        self.product_stream.for_each(self, find_links_to_products)

    def stop(self):
        self.messages_stream.unregister_all(self)
        self.ad_stream.unregister_all(self)
        self.product_stream.unregister_all(self)
