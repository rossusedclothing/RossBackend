import json

from cozepy import COZE_CN_BASE_URL

from application.settings import COZE_TOKEN, COZE_WORKFLOW_ID

coze_api_base = COZE_CN_BASE_URL

from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType  # noqa
from loguru import logger


class CozeApi:

    def __init__(self):
        self.coze = Coze(auth=TokenAuth(token=COZE_TOKEN), base_url=coze_api_base)

    def send_foreign_trade_workflow(self, message: str, user_id: str | int, sales_repp_phone: str, sales_agent: str):
        """
        外贸工作流
        """
        workflow = self.coze.workflows.runs.create(
            workflow_id=COZE_WORKFLOW_ID,
            parameters={
                "input": message,
                "user_id": user_id,
                "sales_repp_phone": sales_repp_phone or '0',
                "sales_agent": sales_agent or 'Ross Company Intelligent Assistant',
            })
        logger.info(workflow)
        data = json.loads(workflow.data)
        output = data.get("output")
        user_info = data.get("userInfo")
        if not output:
            # TODO 响应失败请联系客户：user_id
            return ""
        return output, user_info
