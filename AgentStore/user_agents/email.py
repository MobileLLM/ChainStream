import chainstream as cs


class AgentExampleForEmailTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_1"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "summary_by_sender")

        self.llm = cs.llm.get_model("Text")

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

            return list(sender_group.values())

        def sum_by_sender(sender_email):
            sender = sender_email[0]['sender']
            prompt = "Summarize these all email here"
            res = self.llm.query(cs.llm.make_prompt([x['Content'] for x in sender_email], prompt))
            self.email_output.add_item({
                "sender": sender,
                "summary": res
            })

        self.email_input.for_each(filter_ads).batch(by_count=2).for_each(group_by_sender).for_each(sum_by_sender)



