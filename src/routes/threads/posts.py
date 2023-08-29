from src.routes.init_common_route import *
from services.posts_services import *
from src.services.authentication_services import is_a_user

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
@cross_origin()
def posts():
    threads = supabase.table('blog_posts').select("*").execute().data
    return jsonify([thread for thread in threads if thread['parent_comment_id'] is None])   

@posts_bp.route('/posts/<post_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def post(post_id):
    if request.method == 'GET':
        thread = get_thread(post_id)
        return jsonify(thread)
    elif request.method == 'PUT':
        data = request.get_json()
        title = data['title']
        content = data['content']
        result = update_thread(post_id, title, content)
        supabase.table('blog_posts').update({'title': title, 'content': content}).eq('post_id', post_id).execute()
        return (f'Success! Thread {post_id} has been updated')
    elif request.method == 'DELETE':
        result = delete_thread(post_id)
        return result


@posts_bp.route('/posts/user/<username>', methods=['GET'])
@cross_origin()
def user_posts(username):
    threads = supabase.table('blog_posts').select("*").eq('username', username).execute().data
    return jsonify([thread for thread in threads if thread['parent_comment_id'] is None])

@posts_bp.route('/create_post', methods=['POST'])
@cross_origin()
def create_post():
    data = request.get_json() 
    user = data['user']
    title = data['title']
    content = data['content']

    try:
        supabase.table('blog_posts').insert( {"title": title, "content": content, "username": user} ).execute()
        return 'good boy'
    except:
        return 'Failed. Reason: Invalid data'
    
@posts_bp.route('/add_like/<user>/<post_id>', methods=['GET'])
@cross_origin()
def add_like(user, post_id):
    result = update_post_likes(post_id, user)
    return result

@posts_bp.route('/remove_like/<user>/<post_id>', methods=['GET'])
@cross_origin()
def remove_like(user, post_id):
    result = remove_post_likes(post_id, user)
    return result