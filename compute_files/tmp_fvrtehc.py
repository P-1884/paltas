# coding=utf-8
def outer_factory():
    kwargs_detector = None
    learning_params = None
    log_learning_params = None
    noise_function = None
    norm_dict = None
    norm_images = None

    def inner_factory(ag__):

        def tf__parse_image_features(example):
            with ag__.FunctionScope('parse_image_features', 'fscope', ag__.STD) as fscope:
                do_return = False
                retval_ = ag__.UndefinedReturnValue()
                data_features = {'image': ag__.converted_call(ag__.ld(tf).io.FixedLenFeature, ([], ag__.ld(tf).string), None, fscope), 'height': ag__.converted_call(ag__.ld(tf).io.FixedLenFeature, ([], ag__.ld(tf).int64), None, fscope), 'width': ag__.converted_call(ag__.ld(tf).io.FixedLenFeature, ([], ag__.ld(tf).int64), None, fscope), 'index': ag__.converted_call(ag__.ld(tf).io.FixedLenFeature, ([], ag__.ld(tf).int64), None, fscope)}

                def get_state():
                    return (log_learning_params_list,)

                def set_state(vars_):
                    nonlocal log_learning_params_list
                    (log_learning_params_list,) = vars_

                def if_body():
                    nonlocal log_learning_params_list
                    log_learning_params_list = []

                def else_body():
                    nonlocal log_learning_params_list
                    log_learning_params_list = ag__.ld(log_learning_params)
                log_learning_params_list = ag__.Undefined('log_learning_params_list')
                ag__.if_stmt((ag__.ld(log_learning_params) is None), if_body, else_body, get_state, set_state, ('log_learning_params_list',), 1)

                def get_state_1():
                    return ()

                def set_state_1(block_vars):
                    pass

                def loop_body(itr):
                    param = itr
                    ag__.ld(data_features)[ag__.ld(param)] = ag__.converted_call(ag__.ld(tf).io.FixedLenFeature, ([], ag__.ld(tf).float32), None, fscope)
                param = ag__.Undefined('param')
                ag__.for_stmt((ag__.ld(learning_params) + ag__.ld(log_learning_params_list)), None, loop_body, get_state_1, set_state_1, (), {'iterate_names': 'param'})
                parsed_dataset = ag__.converted_call(ag__.ld(tf).io.parse_single_example, (ag__.ld(example), ag__.ld(data_features)), None, fscope)
                image = ag__.converted_call(ag__.ld(tf).io.decode_raw, (ag__.ld(parsed_dataset)['image'],), dict(out_type=ag__.ld(float)), fscope)
                image = ag__.converted_call(ag__.ld(tf).reshape, (ag__.ld(image), (ag__.ld(parsed_dataset)['height'], ag__.ld(parsed_dataset)['width'], 1)), None, fscope)

                def get_state_2():
                    return (image,)

                def set_state_2(vars_):
                    nonlocal image
                    (image,) = vars_

                def if_body_1():
                    nonlocal image
                    image = ag__.ld(image)
                    image += ag__.converted_call(noise_function, (image, kwargs_detector), None, fscope)

                def else_body_1():
                    nonlocal image
                    pass
                ag__.if_stmt((ag__.ld(noise_function) is not None), if_body_1, else_body_1, get_state_2, set_state_2, ('image',), 1)

                def get_state_3():
                    return (image,)

                def set_state_3(vars_):
                    nonlocal image
                    (image,) = vars_

                def if_body_2():
                    nonlocal image
                    image = (ag__.ld(image) / ag__.converted_call(ag__.ld(tf).math.reduce_std, (ag__.ld(image),), None, fscope))

                def else_body_2():
                    nonlocal image
                    pass
                ag__.if_stmt(ag__.ld(norm_images), if_body_2, else_body_2, get_state_3, set_state_3, ('image',), 1)

                def get_state_4():
                    return ()

                def set_state_4(block_vars):
                    pass

                def loop_body_1(itr_1):
                    param = itr_1
                    ag__.ld(parsed_dataset)[ag__.ld(param)] = ag__.converted_call(ag__.ld(tf).math.log, (ag__.ld(parsed_dataset)[ag__.ld(param)],), None, fscope)
                ag__.for_stmt(ag__.ld(log_learning_params_list), None, loop_body_1, get_state_4, set_state_4, (), {'iterate_names': 'param'})

                def get_state_6():
                    return ()

                def set_state_6(block_vars):
                    pass

                def if_body_3():

                    def get_state_5():
                        return ()

                    def set_state_5(block_vars):
                        pass

                    def loop_body_2(itr_2):
                        param = itr_2
                        ag__.ld(parsed_dataset)[ag__.ld(param)] -= ag__.ld(norm_dict)['mean'][ag__.ld(param)]
                        ag__.ld(parsed_dataset)[ag__.ld(param)] /= ag__.ld(norm_dict)['std'][ag__.ld(param)]
                    ag__.for_stmt((ag__.ld(learning_params) + ag__.ld(log_learning_params_list)), None, loop_body_2, get_state_5, set_state_5, (), {'iterate_names': 'param'})

                def else_body_3():
                    pass
                ag__.if_stmt((ag__.ld(norm_dict) is not None), if_body_3, else_body_3, get_state_6, set_state_6, (), 0)
                lens_param_values = ag__.converted_call(ag__.ld(tf).stack, ([ag__.ld(parsed_dataset)[ag__.ld(param)] for param in (ag__.ld(learning_params) + ag__.ld(log_learning_params_list))],), None, fscope)
                try:
                    do_return = True
                    retval_ = (ag__.ld(image), ag__.ld(lens_param_values))
                except:
                    do_return = False
                    raise
                return fscope.ret(retval_, do_return)
        return tf__parse_image_features
    return inner_factory