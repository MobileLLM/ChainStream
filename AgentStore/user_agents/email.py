import chainstream as cs
import threading
import time


class AgentExampleForEmailTask1(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id="agent_example_for_email_task_1"):
        super().__init__(agent_id)
        self.email_input = cs.create_stream(self, "all_email")
        self.email_output = cs.create_stream(self, "summary_by_sender")
        # self.email_output = cs.create_stream(self, {
        #     "stream_id": "summary_by_sender",
        #     "description": "A list of email summaries for each email sender, excluding ads",
        #     "fields": {
        #         "sender": "name xxx, string",
        #         "summary": "sum xxx, string"
        #     }
        # })

        self.llm = cs.llm.get_model("Text")

        self.sendding = False
        self.threader = threading.Thread(target=self.put_email)


    def put_email(self):
        time.sleep(10)
        while self.sendding:
            for i in range(50):
                time.sleep(1)
                self.email_input.add_item({
                    "sender": "xxx",
                    "Content": "Hi mike, how are you?"}
                )
                if i % 3 == 0:
                    self.email_input.add_item({
                        "sender": "yyy",
                        "Content": "Buy our product today! It's amazing!"

                    })

    def start(self):
        def filter_ads(email):
            prompt = "is this email an advertisement? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            print("filter_ads", res)
            if res.lower() == 'n':
                return email

        def group_by_sender(email_list):
            email_list = email_list['item_list']
            sender_group = {}
            for email in email_list:
                if email['sender'] not in sender_group:
                    sender_group[email['sender']] = [email]
                else:
                    sender_group[email['sender']].append(email)

            print("group_by_sender", list(sender_group.values()))
            return list(sender_group.values())

        def sum_by_sender(sender_email):
            sender = sender_email[0]['sender']
            prompt = "Summarize these all email here"
            print("sum_by_sender: query", [x['Content'] for x in sender_email], prompt)
            res = self.llm.query(cs.llm.make_prompt([x['Content'] for x in sender_email], prompt))
            print("sum_by_sender", res)
            self.email_output.add_item({
                "sender": sender,
                "summary": res
            })

        self.email_input.for_each(filter_ads).batch(by_count=2).for_each(group_by_sender).for_each(sum_by_sender)
        self.sendding = True
        self.threader.start()

    def stop(self):
        self.sendding = False
        self.threader.join()
