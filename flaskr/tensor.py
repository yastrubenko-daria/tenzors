from flask import  Blueprint, g, request, url_for, render_template
from flaskr.models import Vector, Tensor, Mapping_tensor, Rotation_tensor


bp = Blueprint('tensor', __name__, url_prefix='/tensor')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/calculator', methods=["GET", "POST"])
def calculator():
    #user=get_user(user_id)
    if request.method =="POST":
        A = request.form['tensor_A']
        B = request.form['tensor_B']
        a = request.form['vector']
        #plane = request.form['plane']
        operation = request.form['operation']
        #todo: подумать над ошибками 1) вдруг всё пустое-> вывод строчки
        #todo: пустая строка в A условия ввода
        if A != '0':
            A=Tensor(A)
        if B != '0':
            B=Tensor(B)
        if a != '0':
            a=Vector(a)
        if operation == "vector":
            if B == '0':
                return render_template('tensor/calculator.html',ten=True, vec=False,user=g.user, user_id=g.user['id'])
            C=A.vector(B)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=A, B=B, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "scalar":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            C=A.scalar(B)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=A, B=B, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "mult_scal_vec":
            if a == '0':
                return render_template('tensor/calculator.html', ten=False, vec=True,user=g.user, user_id=g.user['id'])
            b=A.mult_scal_vec(a)
            if b != 0:
                b=b.vec
            return render_template('tensor/result.html', A=A, a=a, b=b, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "mult_vect_vec":
            if a == '0':
                return render_template('tensor/calculator.html', ten=False, vec=True,user=g.user, user_id=g.user['id'])
            C=A.mult_vect_vec(a)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=A, a=a, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "double_scalar":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            num=A.double_scalar(B)
            return render_template('tensor/result.html', A=A, B=B, num=num, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "double_vector":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            C=A.double_vector(B)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=A, B=B, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "scalar_vector":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            b=A.scalar_vector(B)
            if b != 0:
                b=b.vec
            return render_template('tensor/result.html', A=A, B=B, b=b, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "vector_scalar":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            b=A.vector_scalar(B)
            if b != 0:
                b=b.vec
            return render_template('tensor/result.html', A=A, B=B, b=b, operation=operation,user=g.user, user_id=g.user['id'])

        if operation == "vector_inv":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            C=B.vector(A)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=B, B=A, C=C, operation='vector',user=g.user, user_id=g.user['id'])
        if operation == "scalar_inv":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            C=B.scalar(A)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=B, B=A, C=C, operation='scalar',user=g.user, user_id=g.user['id'])
        if operation == "mult_scal_tens":
            if a == '0':
                return render_template('tensor/calculator.html', ten=False, vec=True,user=g.user, user_id=g.user['id'])
            b=a.mult_scal_tens(A)
            if b != 0:
                b=b.vec
            return render_template('tensor/result.html', A=A, a=a, b=b, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "mult_vect_tens":
            if a == '0':
                return render_template('tensor/calculator.html', ten=False, vec=True,user=g.user, user_id=g.user['id'])
            C=a.mult_vect_tens(A)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=A, a=a, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "double_scalar_inv":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            num=B.double_scalar(A)
            return render_template('tensor/result.html', A=B, B=A, num=num, operation="double_scalar",user=g.user, user_id=g.user['id'])
        if operation == "double_vector_inv":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            C=B.double_vector(A)
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=B, B=A, C=C, operation='double_vector',user=g.user, user_id=g.user['id'])
        if operation == "scalar_vector_inv":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            b=B.scalar_vector(A)
            if b != 0:
                b=b.vec
            return render_template('tensor/result.html', A=B, B=A, b=b, operation='scalar_vector',user=g.user, user_id=g.user['id'])
        if operation == "vector_scalar_inv":
            if B == '0':
                return render_template('tensor/calculator.html', ten=True, vec=False,user=g.user, user_id=g.user['id'])
            b=B.vector_scalar(A)
            if b != 0:
                b=b.vec
            return render_template('tensor/result.html', A=B, B=A, b=b, operation='vector_scalar',user=g.user, user_id=g.user['id'])

        if operation == "transpose":
            C=A.transpose()
            if C != 0:
                C=C.tensor
            return render_template('tensor/result.html', A=A, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "antisymmetrical":
            C = A.antisymmetrical()
            if C != 0:
                C = C.tensor
            return render_template('tensor/result.html', A=A, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "symmetrical":
            C=A.symmetrical()
            if C != 0:
                C = C.tensor
            return render_template('tensor/result.html',A=A, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "first_invariant":
            num=A.first_invariant()
            return render_template('tensor/result.html', A=A, num=num, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "second_invariant":
            num=A.second_invariant()
            return render_template('tensor/result.html', A=A, num=num, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "third_invariant":
            num=A.third_invariant()
            return render_template('tensor/result.html', A=A, num=num, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "vector_invariant":
            b=A.vector_invariant()
            if b != 0:
                b = b.vec
            return render_template('tensor/result.html', A=A, b=b, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "second_degree":
            C=A.second_degree()
            if C != 0:
                C = C.tensor
            return render_template('tensor/result.html', A=A, C=C, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "inverse":
            C=A.inverse()
            if C != 0:
                C = C.tensor
            return render_template('tensor/result.html', A=A, C=C, operation=operation, user=g.user, user_id=g.user['id'])


    return render_template('tensor/calculator.html', user=g.user, user_id=g.user['id'])


@bp.route('/calculator/rotation', methods=["GET", "POST"])
def calculator_rotation():
    if request.method =="POST":
        P = request.form['tensor_P']
        angle = request.form['angle']
        vec = request.form['rotation_vector']
        a = request.form['vector']
        #plane = request.form['plane']
        operation = request.form['operation']
        #todo: подумать над ошибками 1) вдруг всё пустое-> вывод строчки
        #todo: пустая строка в A условия ввода
        if P != '0':
            P=Rotation_tensor(P)
        if vec != '0':
            vec=Vector(vec)
        if a != '0':
            a=Vector(a)
        if operation == "rotation":
            if P == '0':
                if angle=='0' or vec=='0':
                    return render_template('tensor/rotation.html',ten=True, vec=False, flag=True, user=g.user, user_id=g.user['id'])
                else:
                    P=Rotation_tensor(vec=vec, angle=angle)
            if a != '0':
                return render_template('tensor/rotation.html', ten=False, vec=True, flag=False, user=g.user, user_id=g.user['id'])
            b=P.mult_scal_vec(a)
            if b != 0:
                b=b.vec
            return render_template('tensor/result.html', A=P, a=a, b=b, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "find_angle":
            if P == '0':
                return render_template('tensor/rotation.html',ten=True, vec=False, flag=False,user=g.user, user_id=g.user['id'])
            angle=P.angle
            return render_template('tensor/result.html', A=P, angle=angle, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "find_vec":
            if P == '0':
                return render_template('tensor/calculator.html',ten=True, vec=False, flag=False,user=g.user, user_id=g.user['id'])
            vec = P.vec
            return render_template('tensor/result.html', A=P, vec=vec, operation=operation,user=g.user, user_id=g.user['id'])
        if operation == "find_rot_tensor":
            if angle == '0' or vec == '0':
                return render_template('tensor/rotation.html', ten=False, vec=False, flag=True,user=g.user, user_id=g.user['id'])
            else:
                P = Rotation_tensor(vec=vec, angle=angle)
            return render_template('tensor/result.html', A=P, operation=operation,user=g.user, user_id=g.user['id'])

    return render_template('tensor/rotation.html', user=g.user, user_id=g.user['id'])