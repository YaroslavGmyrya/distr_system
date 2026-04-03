import grpc
from concurrent import futures

import service_pb2
import service_pb2_grpc


class ServiceImplementation(service_pb2_grpc.TasksServiceServicer):
    def MyMethod(self, request, context):
        
        response_text = f"Получен id: {request.id}"
        return service_pb2.MyResponse(result=response_text)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    service_pb2_grpc.add_TasksServiceServicer_to_server(
        ServiceImplementation(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("gRPC server started on port 50051")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()