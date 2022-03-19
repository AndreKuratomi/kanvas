from django.test import TestCase, TransactionTestCase
from rest_framework.test import APIClient


class TestAccountsRoutesWithoutAuthentication(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.instructor_data = {
            "first_name": "Instructor",
            "last_name": "Kenzie",
            "email": "instructor@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }
        
        self.instructor_wrong_data = {
            "name": "Instructor",
            "email": "instructor@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }

        self.instructor_login_data = {
            "email": "instructor@kenzie.com.br",
            "password": "kenzie"
        }

        self.instructor_login_wrong_data = {
            "email": "instructor@kenzie.com.br",
            "password": "12345"
        }

        self.instructor_login_wrong_field = {
            "username": "instructor@kenzie.com.br",
            "password": "12345"
        }

        self.student_data = {
            "first_name": "Student",
            "last_name": "Kenzie",
            "email": "student@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }

        self.student_login_data = {
            "email": "student@kenzie.com.br",
            "password": "kenzie"
        }
    
    def test_instructor_user_creation_201(self):
        # Criando um usuário do tipo Instructor
        response = self.client.post("/api/accounts/", self.instructor_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(output["first_name"], self.instructor_data["first_name"])
        self.assertEqual(output["is_admin"], self.instructor_data["is_admin"])
        self.assertIn("uuid", output)
        self.assertNotIn("password", output)
        

    def test_student_user_creation_201(self):
        # Criando um usuário do tipo Student
        response = self.client.post("/api/accounts/", self.student_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(output["first_name"], self.student_data["first_name"])
        self.assertEqual(output["is_admin"], self.student_data["is_admin"])
        self.assertIn("uuid", output)
        self.assertNotIn("password", output)


    def test_duplicate_email_user_creation_422(self):
        # Tentando criar dois usuários com os mesmos dados. O segundo deve ser bloqueado
        self.client.post("/api/accounts/", self.instructor_data, format="json")
        response = self.client.post("/api/accounts/", self.instructor_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(output, {'message': 'User already exists'}) 

        # Logando com instructor para listar usuários
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Checando se o usuário duplicado realmente não foi criado no banco
        response_users = self.client.get("/api/accounts/", format="json")
        self.assertEqual(response_users.status_code, 200)
        self.assertEqual(len(response_users.json()), 1)

    
    def test_wrong_data_user_creation_400(self):
        # Tentando criar um usuário com campos incorretos
        response = self.client.post("/api/accounts/", self.instructor_wrong_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", output) 
        self.assertIn("last_name", output) 

        # Criando e logando com instructor para listar usuários
        self.client.post("/api/accounts/", self.instructor_data, format="json")
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Checando se o usuário realmente não foi criado no banco
        response_users = self.client.get("/api/accounts/", format="json")
        self.assertEqual(response_users.status_code, 200)
        self.assertEqual(len(response_users.json()), 1) 
        # o tamanho 1 é por conta do intructor criado para logar 

    
    def test_login_success_200(self):
        # Criando um usuário do tipo Instructor e tentando logar com suas credenciais corretas
        self.client.post("/api/accounts/", self.instructor_data, format="json")

        response = self.client.post("/api/login/", self.instructor_login_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", output)


    def test_login_with_invalid_credentials_401(self):
        # Criando um usuário do tipo Instructor e tentando logar com suas credenciais erradas
        self.client.post("/api/accounts/", self.instructor_data, format="json")
        response = self.client.post("/api/login/", self.instructor_login_wrong_data, format="json")

        self.assertEqual(response.status_code, 401)

        try:
            output = response.json()
            self.assertNotIn("token", output)
        except TypeError:
            pass


    def test_login_with_wrong_fields_400(self):
        # Criando um usuário do tipo Instructor e tentando logar com o campo username no lugar de email
        self.client.post("/api/accounts/", self.instructor_data, format="json")
        response = self.client.post("/api/login/", self.instructor_login_wrong_field, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", output)

    
    def test_list_users_by_instructor_200(self):
        # Criando instructor e logando com ele
        self.client.post("/api/accounts/", self.instructor_data, format="json")
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # O usuário criado deve ser o único na listagem
        response = self.client.get("/api/accounts/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["email"], self.instructor_data["email"])


    def test_list_users_by_student_403(self):
        # Criando student e logando com ele
        self.client.post("/api/accounts/", self.student_data, format="json")
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # O student não deve ter permissão para listar usuários
        response = self.client.get("/api/accounts/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {'detail': 'You do not have permission to perform this action.'})

    def test_list_users_with_no_token_401(self):
        # Tentando listar usuários sem passar um token na requisição
        response = self.client.get("/api/accounts/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, {'detail': 'Authentication credentials were not provided.'})



class TestCoursesCreation(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()

        # Criando instructor
        self.instructor_data = {
            "first_name": "Instructor",
            "last_name": "Kenzie",
            "email": "instructor@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }
        self.client.post("/api/accounts/", self.instructor_data, format="json")

        # Criando student 
        self.student_data = {
            "first_name": "Student",
            "last_name": "Kenzie",
            "email": "student@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }
        self.client.post("/api/accounts/", self.student_data, format="json")


        self.student_login_data = {
            "email": "student@kenzie.com.br",
            "password": "kenzie"
        }
        
        self.instructor_login_data = {
            "email": "instructor@kenzie.com.br",
            "password": "kenzie"
        }


        self.course_data = {
            "name": "Django",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/django_demos",
        }

        self.course_data_wrong = {
            "course_name": "Django",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/django_demos",
        }      

        self.course_data_update = {
            "name": "Node",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/node_demos",
        }  



    def test_course_creation_by_instructor_201(self):
        # Logando com intructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post("/api/courses/", self.course_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("uuid", output)
        self.assertEqual(output["name"], self.course_data["name"])
        self.assertIn("instructor", output)
        self.assertIsNone(output["instructor"])


    def test_course_creation_by_student_403(self):
        # Logando com student
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Student não deve ter permissão de criar o curso
        response = self.client.post("/api/courses/", self.course_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {'detail': 'You do not have permission to perform this action.'})

        # Checando se o curso realmente não foi criado no banco
        response_courses = self.client.get("/api/courses/", format="json")
        self.assertEqual(response_courses.status_code, 200)
        self.assertEqual(len(response_courses.json()), 0)


    def test_course_creation_by_no_user_401(self):
        # Tentando listar cursos sem autenticação
        response = self.client.post("/api/courses/", self.course_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, {'detail': 'Authentication credentials were not provided.'})

        # Checando se o curso realmente não foi criado no banco
        response_courses = self.client.get("/api/courses/", format="json")
        self.assertEqual(response_courses.status_code, 200)
        self.assertEqual(len(response_courses.json()), 0)


    def test_course_creation_duplicate_name_422(self):
        # Logando com intructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/courses/", self.course_data, format="json")
        response = self.client.post("/api/courses/", self.course_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(output, {'message': 'Course already exists'})

        # Checando se o segundo curso realmente não foi criado no banco
        response_courses = self.client.get("/api/courses/", format="json")
        self.assertEqual(response_courses.status_code, 200)
        self.assertEqual(len(response_courses.json()), 1)


    def test_course_creation_wrong_data_400(self):
        # Logando com intructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post("/api/courses/", self.course_data_wrong, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", output)

        # Checando se o segundo curso realmente não foi criado no banco
        response_courses = self.client.get("/api/courses/", format="json")
        self.assertEqual(response_courses.status_code, 200)
        self.assertEqual(len(response_courses.json()), 0)


    def test_list_courses_200(self):
        response = self.client.get("/api/courses/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(output, [])

        # Logando com intructor para criar um curso
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.client.post("/api/courses/", self.course_data, format="json")

        # Limpando token do client
        self.client.credentials()

        response = self.client.get("/api/courses/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["name"], self.course_data["name"])


    def test_retrieve_valid_course_200(self):
        # Logando com instructor para criar um curso
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        course = self.client.post("/api/courses/", self.course_data, format="json").json()

        # Limpando token do client
        self.client.credentials()

        # Buscando por um curso com id inexistente 
        uuid = course["uuid"]
        response = self.client.get(f"/api/courses/{uuid}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(output, course)


    def test_retrieve_invalid_course_404(self):
        # Buscando por um curso com id inexistente 
        uuid = "9ec9ef8a-2a2f-4ff3-b007-406d9ef2fc63"
        response = self.client.get(f"/api/courses/{uuid}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(output, {'message': 'Course does not exist'})


class TestCoursesUpdate(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()

        # Criando instructor
        self.instructor_data = {
            "first_name": "Instructor",
            "last_name": "Kenzie",
            "email": "instructor@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }
        self.client.post("/api/accounts/", self.instructor_data, format="json")

        self.instructor_login_data = {
            "email": "instructor@kenzie.com.br",
            "password": "kenzie"
        }

        self.course_data = {
            "name": "Django",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/django_demos",
        }

        # Logando com instructor para criar um curso
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Pegando o ID do curso criado
        self.course_id = self.client.post("/api/courses/", self.course_data, format="json").json()["uuid"]

        # Criando student 
        self.student_data = {
            "first_name": "Student",
            "last_name": "Kenzie",
            "email": "student@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }
        self.client.post("/api/accounts/", self.student_data, format="json")

        self.student_login_data = {
            "email": "student@kenzie.com.br",
            "password": "kenzie"
        }
        
        # Criando dados de curso para testar
        self.course_data_update = {
            "name": "Node",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/node_demos",
        }  


        # Limpando as credenciais de instrutor do client
        self.client.credentials()


    def test_update_course_by_instructor_200(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Tentando atualizar o curso já criado
        uuid = self.course_id
        response = self.client.patch(f"/api/courses/{uuid}/", self.course_data_update, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["uuid"], uuid)
        self.assertEqual(output["name"], str(self.course_data_update["name"]))


    def test_update_course_by_student_403(self):
        # Logando com student
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Tentando atualizar o curso já criado
        uuid = self.course_id
        response = self.client.patch(f"/api/courses/{uuid}/", self.course_data_update, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {'detail': 'You do not have permission to perform this action.'})

        # Checando se o curso realmente não foi alterado no banco
        response_course = self.client.get(f"/api/courses/{uuid}/", format="json")

        self.assertEqual(response_course.status_code, 200)
        self.assertNotEqual(response_course.json()["name"], str(self.course_data_update["name"]))


    def test_update_course_by_no_user_401(self):
        # Tentando atualizar o curso já criado
        uuid = self.course_id
        response = self.client.patch(f"/api/courses/{uuid}/", self.course_data_update, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, {'detail': 'Authentication credentials were not provided.'})

        # Checando se o curso realmente não foi alterado no banco
        response_course = self.client.get(f"/api/courses/{uuid}/", format="json")

        self.assertEqual(response_course.status_code, 200)
        self.assertNotEqual(response_course.json()["name"], str(self.course_data_update["name"]))


    def test_update_invalid_course_404(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Tentando atualizar um curso com id inválido
        uuid = "0bedf5fc-98cd-42ae-83ce-71fc006c0d29"
        response = self.client.patch(f"/api/courses/{uuid}/", self.course_data_update, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(output, {'message': 'Course does not exist'})

        # Checando se o curso realmente não foi alterado no banco
        response_course = self.client.get(f"/api/courses/{self.course_id}/", format="json")

        self.assertEqual(response_course.status_code, 200)
        self.assertNotEqual(response_course.json()["name"], str(self.course_data_update["name"]))


    def test_update_course_with_conflict_422(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        uuid = self.course_id

        # Criando um segundo curso no banco, com as informações que serão utilizadas na atualização do primeiro
        self.client.post("/api/courses/", self.course_data_update, format="json")

        # Tentando atualizar o primeiro curso com as informações do segundo
        response = self.client.patch(f"/api/courses/{uuid}/", self.course_data_update, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(output, {'message': 'This course name already exists'})

        # Checando se o curso realmente não foi alterado no banco
        response_course = self.client.get(f"/api/courses/{uuid}/", format="json")

        self.assertEqual(response_course.status_code, 200)
        self.assertNotEqual(response_course.json()["name"], str(self.course_data_update["name"]))



class TestCoursesRegister(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()

        # Criando instructor
        self.instructor_data = {
            "first_name": "Instructor",
            "last_name": "Kenzie",
            "email": "instructor@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }
        # Pegando id de instructor criado
        self.instructor_id = self.client.post("/api/accounts/", self.instructor_data, format="json").json()["uuid"]

        self.instructor_data_2 = {
            "first_name": "Instructor_2",
            "last_name": "Kenzie",
            "email": "instructor2@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }

        # Criando student 
        self.student_data = {
            "first_name": "Student",
            "last_name": "Kenzie",
            "email": "student@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }
        # Pegando id de student criado
        self.student_id = self.client.post("/api/accounts/", self.student_data, format="json").json()["uuid"]

        self.student_data_2 = {
            "first_name": "Student_2",
            "last_name": "Kenzie",
            "email": "student2@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }
        # Pegando id de student 2 criado
        self.student_id_2 = self.client.post("/api/accounts/", self.student_data_2, format="json").json()["uuid"]


        self.student_login_data = {
            "email": "student@kenzie.com.br",
            "password": "kenzie"
        }
        
        self.instructor_login_data = {
            "email": "instructor@kenzie.com.br",
            "password": "kenzie"
        }


        self.course_data = {
            "name": "Django",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/django_demos",
        }

        self.course_data_update = {
            "name": "Node",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/node_demos",
        }


        # Logando com instructor para criar um curso
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Pegando o ID do curso criado
        self.course_id = self.client.post("/api/courses/", self.course_data, format="json").json()["uuid"]

        # Limpando as credenciais de instrutor do client
        self.client.credentials()



    def test_register_instructor_course_by_instructor_200(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        body = {
            "instructor_id": self.instructor_id
        }

        # Tentando registrar o instructor no curso já criado
        response = self.client.put(f"/api/courses/{course_id}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("instructor", output)
        self.assertIsNotNone(output["instructor"])
        self.assertEqual(output["instructor"]["uuid"], self.instructor_id)

        # Checando se o instructor realmente foi relacionado ao curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNotNone(course_response["instructor"])
        self.assertEqual(course_response["instructor"]["uuid"], self.instructor_id)

        # Criando um segundo curso no banco
        course_id_2 = self.client.post("/api/courses/", self.course_data_update, format="json").json()["uuid"]

        # Tentando registrar o instructor no segundo curso
        response = self.client.put(f"/api/courses/{course_id_2}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("instructor", output)
        self.assertIsNotNone(output["instructor"])
        self.assertEqual(output["instructor"]["uuid"], self.instructor_id)

        # verificando se o primeiro curso deixou de ter o instrutor
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNone(course_response["instructor"])

        # Criando outro instructor para registrar no lugar do primeiro
        instructor_2_uuid = self.client.post("/api/accounts/", self.instructor_data_2, format="json").json()["uuid"]

        body_2 = {
            "instructor_id": instructor_2_uuid
        }

        # Tentando registrar o instructor_2 no segundo curso
        response = self.client.put(f"/api/courses/{course_id_2}/registrations/instructor/", body_2, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["instructor"]["uuid"], str(instructor_2_uuid))


    def test_register_instructor_course_by_student_403(self):
        # Logando com student
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
       
        # Id do curso já criado
        course_id = self.course_id

        body = {
            "instructor_id": self.instructor_id
        }

        # Tentando registrar o student
        response = self.client.put(f"/api/courses/{course_id}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {'detail': 'You do not have permission to perform this action.'})
        
        # Checando se realmente não houve alteração do curso no banco
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNone(course_response["instructor"])


    def test_register_instructor_course_by_no_user_401(self):
        # Id do curso já criado
        course_id = self.course_id

        body = {
            "instructor_id": self.instructor_id
        }

        # Tentando registrar o student
        response = self.client.put(f"/api/courses/{course_id}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, {'detail': 'Authentication credentials were not provided.'})
        
        # Checando se realmente não houve alteração do curso no banco
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNone(course_response["instructor"])


    def test_register_instructor_course_wrong_courseId_404(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # course_id invalido
        course_id = "3c999254-d9b5-4bfc-a585-3e8e1f8d5151"

        body = {
            "instructor_id": self.instructor_id
        }

        # Tentando registrar o instructor
        response = self.client.put(f"/api/courses/{course_id}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(output, {'message': 'Course does not exist'})


    def test_register_instructor_course_with_student_id_422(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        body = {
            "instructor_id": self.student_id
        }

        # Tentando registrar o instructor
        response = self.client.put(f"/api/courses/{course_id}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(output, {'message': 'Instructor id does not belong to an admin'})

        # Checando se realmente não houve alteração do curso no banco
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNone(course_response["instructor"])


    def test_register_instructor_course_with_invalid_id_404(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        # Instructor_id invalido
        body = {
            "instructor_id": "49946481-3b89-424c-9581-80ffdf74a23c"
        }

        # Tentando registrar o instructor
        response = self.client.put(f"/api/courses/{course_id}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(output, {'message': 'Invalid instructor_id'})

        # Checando se realmente não houve alteração do curso no banco
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNone(course_response["instructor"])


    def test_register_instructor_course_with_wrong_field_400(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        # Enviando body com nome do campo errado (instructor_id)
        body = {
            "instructor": self.instructor_id
        }

        # Tentando registrar o instructor
        response = self.client.put(f"/api/courses/{course_id}/registrations/instructor/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("instructor_id", output)

        # Checando se realmente não houve alteração do curso no banco
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNone(course_response["instructor"])


    def test_register_students_course_by_intructor_200(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        # Criando segundo student 
        self.client.post("/api/accounts/", self.student_data_2, format="json")

        # Body com id dos estudantes
        body = {
            "students_id": [self.student_id, self.student_id_2]
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("students", output)
        self.assertIsNotNone(output["students"])

        # Checando se os dois students estão no curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertIsNot(course_response["students"], [])
        users_response = self.client.get("/api/accounts/", format="json").json()
        students = [user for user in users_response if not user["is_admin"]]
        self.assertIn(students[0], course_response["students"])
        self.assertIn(students[1], course_response["students"])

        # Criando segundo curso para também registrar os students 
        course_2_id = self.client.post("/api/courses/", self.course_data_update, format="json").json()["uuid"]

        # Tentando registrar os students no segundo curso
        response = self.client.put(f"/api/courses/{course_2_id}/registrations/students/", body, format="json")
        output = response.json()

        # Checando se os dois students estão no segundo curso
        course_response_2 = self.client.get(f"/api/courses/{course_2_id}/", format="json").json()
        self.assertIsNot(course_response_2["students"], [])
        self.assertIn(students[0], course_response_2["students"])
        self.assertIn(students[1], course_response_2["students"])


    def test_register_students_course_by_student_403(self):
        # Logando com student
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        # Body com id de student
        body = {
            "students_id": [self.student_id]
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {'detail': 'You do not have permission to perform this action.'})

        # Checando se estudante realmente não foi registrade no curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertEqual(course_response["students"], [])


    def test_register_students_course_by_no_user_401(self):

        # Id do curso já criado
        course_id = self.course_id

        # Body com id de student
        body = {
            "students_id": [self.student_id]
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, {'detail': 'Authentication credentials were not provided.'})

        # Checando se estudante realmente não foi registrade no curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertEqual(course_response["students"], [])


    def test_register_students_course_invalid_course_id_404(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Invalid course_id
        course_id = "7506f696-6c36-4ed1-abc4-047911a53cb7"

        # Body com id de student
        body = {
            "students_id": [self.student_id]
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(output, {'message': 'Course does not exist'})

        # Checando se estudante realmente não foi registrade no curso
        course_response = self.client.get(f"/api/courses/{self.course_id}/", format="json").json()
        self.assertEqual(course_response["students"], [])


    def test_register_students_course_with_invalid_student_id_404(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        # Body com student_id invalido
        body = {
            "students_id": ["d0495ae5-7b7c-42b4-af28-7d386f2aaca7"]
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(output, {'message': 'Invalid students_id list'}) 

        # Checando se estudante realmente não foi registrade no curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertEqual(course_response["students"], [])


    def test_register_students_course_with_instructor_id_422(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        # Body com instructor_id 
        body = {
            "students_id": [self.instructor_id]
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(output, {'message': 'Some student id belongs to an Instructor'}) 

        # Checando se instructor realmente não foi registrade no curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertEqual(course_response["students"], [])
        self.assertIsNone(course_response["instructor"])

    def test_register_students_course_with_wrong_field_400(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id
        
        # Body com field name invalido
        body = {
            "students": [self.student_id]
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("students_id", output)

        # Checando se instructor realmente não foi registrade no curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertEqual(course_response["students"], [])


    def test_register_students_course_with_wrong_field_type_400(self):
        # Logando com instructor
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Id do curso já criado
        course_id = self.course_id

        # Body com field type invalido (string)
        body = {
            "students_id": self.student_id
        }

        # Tentando registrar os students
        response = self.client.put(f"/api/courses/{course_id}/registrations/students/", body, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("students_id", output)

        # Checando se instructor realmente não foi registrade no curso
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertEqual(course_response["students"], [])


class TestCourseDelete(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()

        # Criando instructor
        self.instructor_data = {
            "first_name": "Instructor",
            "last_name": "Kenzie",
            "email": "instructor@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }
        self.client.post("/api/accounts/", self.instructor_data, format="json")

        # Criando student 
        self.student_data = {
            "first_name": "Student",
            "last_name": "Kenzie",
            "email": "student@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }
        self.client.post("/api/accounts/", self.student_data, format="json")

        self.student_login_data = {
            "email": "student@kenzie.com.br",
            "password": "kenzie"
        }
        
        self.instructor_login_data = {
            "email": "instructor@kenzie.com.br",
            "password": "kenzie"
        }

        # Logando com instructor para criar um curso
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.course_data = {
            "name": "Django",
            "demo_time": "09:00",
            "link_repo": "https://gitlab.com/django_demos",
        }
        self.course_id = self.client.post("/api/courses/", self.course_data, format="json").json()["uuid"]

        # Limpando as credenciais de instrutor do client
        self.client.credentials()


    def test_delete_course_by_instructor_204(self):
        # Logando com instructor para deletar um curso
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Buscando o curso já criado
        course_id = self.course_id 

        response = self.client.delete(f"/api/courses/{course_id}/", format="json")

        self.assertEqual(response.status_code, 204)

        # Checando se curso realmente foi deletado
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json")
        self.assertEqual(course_response.status_code, 404)


    def test_delete_course_by_student_403(self):
        # Logando com student para deletar um curso
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Buscando o curso já criado
        course_id = self.course_id 

        response = self.client.delete(f"/api/courses/{course_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(output, {'detail': 'You do not have permission to perform this action.'})
        
        # Checando se curso realmente não foi deletado
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json")
        self.assertEqual(course_response.status_code, 200)

    def test_delete_course_by_no_user_401(self):
        # Buscando o curso já criado
        course_id = self.course_id 

        response = self.client.delete(f"/api/courses/{course_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(output, {'detail': 'Authentication credentials were not provided.'})
        
        # Checando se curso realmente não foi deletado
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json")
        self.assertEqual(course_response.status_code, 200)
        self.assertEqual(course_response.json()["uuid"], course_id)


    def test_delete_course_with_invalid_course_id_404(self):
        # Logando com instructor para deletar um curso
        token = self.client.post("/api/login/", self.instructor_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Course_id invalido
        course_id = "e44bc262-d3a2-4917-995c-c3c31ea1a689" 

        response = self.client.delete(f"/api/courses/{course_id}/", format="json")
        output = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(output, {'message': 'Course does not exist'}) 

        # Checando se curso realmente não foi deletado
        course_response = self.client.get(f"/api/courses/{course_id}/", format="json").json()
        self.assertNotEqual(course_response, [])
        self.assertEqual(len(course_response), 1)


class TestAddress(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Criando instructor
        self.instructor_data = {
            "first_name": "Instructor",
            "last_name": "Kenzie",
            "email": "instructor@kenzie.com.br",
            "password": "kenzie",
            "is_admin": True
        }
        self.client.post("/api/accounts/", self.instructor_data, format="json")

        self.instructor_login_data = {
            "email": "instructor@kenzie.com.br",
            "password": "kenzie"
        }

        # Criando student 1
        self.student_data = {
            "first_name": "Student",
            "last_name": "Kenzie",
            "email": "student@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }
        self.client.post("/api/accounts/", self.student_data, format="json")

        self.student_login_data = {
            "email": "student@kenzie.com.br",
            "password": "kenzie"
        }

        # Criando student 2
        self.student_data_2 = {
            "first_name": "Student 2",
            "last_name": "Kenzie",
            "email": "student2@kenzie.com.br",
            "password": "kenzie",
            "is_admin": False
        }
        self.client.post("/api/accounts/", self.student_data_2, format="json")

        self.student_login_data_2 = {
            "email": "student2@kenzie.com.br",
            "password": "kenzie"
        }
        

        self.address_data = {
            "street": "Rua das Orquídeas",
            "house_number": 193,
            "city": "Taubaté",
            "state": "SP",
            "zip_code": "86990-000",
            "country": "Brasil"
        }


        self.address_data_wrong = {
            "street": "Rua das Orquídeas",
            "city": "Taubaté",
            "state": "SP",
            "country": "Brasil"
        }
        

    def test_address_creation_200(self):
        # Logando com student para criar um endereço
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        response = self.client.put("/api/address/", self.address_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("uuid", output)
        self.assertIn("street", output)
        self.assertIn("house_number", output)
        self.assertIn("city", output)
        self.assertIn("state", output)
        self.assertIn("zip_code", output)
        self.assertIn("country", output)
        self.assertIn("users", output)
        self.assertIsNot(output["street"], "")
        self.assertEqual(output["zip_code"], self.address_data["zip_code"])


    def test_address_creation_already_exists_200(self):
        # Logando com student para criar um endereço
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Tentando criar o mesmo endereço duas vezes
        self.client.put("/api/address/", self.address_data, format="json")
        response = self.client.put("/api/address/", self.address_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["zip_code"], self.address_data["zip_code"])
        self.assertEqual(len(output["users"]), 1)

        # Logando com student 2 para tentar criar o mesmo endereço
        token = self.client.post("/api/login/", self.student_login_data_2, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Tentando criar o mesmo endereço, agora por outro user
        self.client.put("/api/address/", self.address_data, format="json")
        response = self.client.put("/api/address/", self.address_data, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["zip_code"], self.address_data["zip_code"])
        self.assertEqual(len(output["users"]), 2)


    def test_address_creation_wrong_data_400(self):
        # Logando com student para criar um endereço
        token = self.client.post("/api/login/", self.student_login_data, format="json").json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Tentando criar o endereço com campos errados
        response = self.client.put("/api/address/", self.address_data_wrong, format="json")
        output = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("uuid", output)
        self.assertNotIn("user", output)
        self.assertIn("house_number", output)
        self.assertIn("zip_code", output)