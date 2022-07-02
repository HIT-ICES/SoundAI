package com.hitices.soundai.controller;

import com.hitices.common.MResponse;
import com.hitices.soundai.bean.SoundBean;
import com.hitices.soundai.util.MRequestUtils;
import com.hitices.soundai.util.MUrlUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping(value = "/soundai")
public class SoundAIController {
    private Logger logger = LogManager.getLogger(SoundAIController.class);

    public SoundAIController() {
    }
    @PostMapping(value = "/detect")
    public MResponse movedetect(@RequestBody SoundBean vedioBean) {
        try {
            MResponse response = MRequestUtils.sendRequest(
                    MUrlUtils.getRemoteUri("127.0.0.1", 12345, "/soundai/detect"),
                    vedioBean,
                    MResponse.class,
                    RequestMethod.POST
            );

            if (response.getCode() == MResponse.successCode) {
                return MResponse.successMResponse().set("message", "请求成功").set("data",response.get("result"));
            }

        }catch (Exception e) {
            logger.debug(e);
            return MResponse.failedMResponse().set("message", "请求失败");
        }
        return MResponse.failedMResponse().set("message", "请求失败");



    }

}
