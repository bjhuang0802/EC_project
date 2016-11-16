grep $1 2501.log|jq -r .session.fid|uniq|xargs -I xx grep 'xx' 2501.log |jq -rc '.|select(.gtm.event == "Purchase")'|nl
