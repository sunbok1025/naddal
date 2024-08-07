from langchain_upstage import UpstageGroundednessCheck


def groundness_check(context, answer):
    # GC
    groundedness_check = UpstageGroundednessCheck()

    request_input = {
        "context": context,
        "answer": answer,
    }
    gc_result = groundedness_check.invoke(request_input)

    print(gc_result)
    if gc_result.lower().startswith("grounded"):
        # print("✅ Groundedness check passed")
        return True
    else:
        # print("❌ Groundedness check failed")
        return False


def pass_answer(thres, chain, icl_examples, question, context):

    for i in range(thres):
        output = chain.invoke(question, icl_examples, context)
        
        # answer = "penguin is so cute"
        if groundness_check(context, output):
            return True, output

    return (
        False,
        "we cannot find the information. Sorry. Can you give me more content for searching? Or you can turn on the option for searching",
    )
