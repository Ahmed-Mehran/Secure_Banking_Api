### --  IMPORTANT IDEA ABOUT MIDDLEWARES WITH AN EXAMPLE(READ IMP) --  watch this video(very imp) (https://www.youtube.com/watch?v=i1nRFHg4q_Y) for better understanding of custom middlewares
## Middleware is a layer that sits between the request coming in and the response going out, touching the request on the way in and the response on the way out. Lets take an example of how the inbuilt authentication
#  middleware works. In a simple JWT auth, tokens are checked for every request, as the user makes the request for login for the first time, the token is not there, then the user is considered as anonymous by the auth
#  middleware and thus asked to login, so logins in with his credentials and matched with DB as well. After the succesfull login, token is created and stored on the client side and then as part of every request this token 
#  is sent(mostly part of headers). So for every new request as this token is present, auth middleware sets this user to authenticated and thus this user can make any new request to a resources which needs to be authenticated
## IN SIMPLE WORDS, In JWT auth, on the first request there is no token, so the authentication middleware can’t identify the user and treats them as anonymous. The user is then required to log in, where the login view checks 
#  the credentials against the database. After a successful login, a JWT token is created and sent to the client. The client stores this token and sends it with every subsequent request, usually in the Authorization header. 
#  On every new request, the authentication middleware reads and verifies the token, extracts the user information from it, and sets request.user as an authenticated user, allowing access to protected resources.
#  We can also return a response in either HTTP or web template form from a middleware directly, its mostly used when the View logic is yet not build i.e your site is under construction.
#  In Django, middleware always works globally — once you add it to MIDDLEWARE in settings, it runs for every request and every view. You cannot attach middleware directly to a single view i.e you cannot have separate 
#  middlewares for individual views. If you want view-specific behavior, Django gives you decorators (like @login_required, @permission_required) or custom decorators, which act like “mini-middleware” but only for that view.
#  So in simple words: middleware is for app-wide logic, and decorators are for per-view logic. Lets understand this custom middle with an example(example from video) first and after that we have our main code
## EXAMPLE CODE : VERY IMPORTANT EXAMPLE WITH INDEPTH EXPLANATION OF HOW MIDDLEWARE WORKS

"""
class MyCLMiddleware:  ## This line defines a custom middleware class. The name can be anything, but by convention it ends with Middleware. Django does not provide this class — you created it. Django will later import this
                        # class when the server starts and treat it as a middleware only because you added it to the MIDDLEWARE list in settings.py. So this class becomes part of Django’s request–response pipeline.
    
    def __init__(self, get_response):            ## This is a special Python method (not Django-specific) that runs once when the Django server starts, not per request. Django itself calls this method and passes in get_response.
                                                  # This method exists so Django can set up the middleware once, instead of rebuilding it for every request. This is why middleware is efficient.
                                                  # get_response is a callable function provided by Django, not something you create. Its job is simple: take a request and return a response.
                                                  # If you have only one middleware, get_response points directly to Django’s view handler — meaning when you call get_response(request), Django immediately calls the view and returns
                                                  # its response. In simple words: when you have only one middleware, get_response is essentially a function that calls the view matched by the URL. So when you do get_response(request),
                                                  # Django immediately runs that view and gives back its response. Just one tiny wording refinement for accuracy: the view itself is not passed into get_response; instead, Django passes
                                                  # a callable wrapper that knows which view to call based on URL resolution(mapping of urls to its view). But conceptually, thinking of it as “the view being called is inside get_response” 
                                                  # is perfectly fine.
                                                  # If you have multiple middlewares, get_response points to the next middleware in the chain, not the view. Each middleware wraps the next one, so calling get_response(request) passes the
                                                  # request forward until the last middleware finally calls the view. This is how Django builds a layered pipeline where every middleware can run code before and after the view without 
                                                  # knowing about the others.
                                                  
        
        self.get_response = get_response          # Here, you are storing a reference to the next step in the pipeline i.e. it can be a view directly if we have single middleware or can be a next middleware in the chain if we have multiple middlewares
                                                  # In that pipeline, each middleware gets a reference to “what should run next.” That “next thing” is passed in as get_response. So get_response is not always the view — it is simply
                                                  # “the next step.” If there are more middlewares below yours, get_response points to the next middleware. If yours is the last middleware, then get_response points directly to the view. 
                                                  # This design allows Django to keep everything flexible and ordered.
        
        print("One Time Initialization")          # This print statement is kind of a proof that the __init__ only runs when the server is started, not with different views but just once when the server starts. You’ll see this printed once in the
                                                  # terminal, even if you refresh the browser 100 times.
        
        
    def __call__(self, request):                  # The __call__ method lets an object be used like a function. Normally, only functions can be called like f(), but if a class has a __call__ method, then after creating an object from that
                                                  # class, you can also do object(), and Python will automatically run the __call__ method. E.g I create an object of class hello() which is obj_hello and this class hello() has __call__ method
                                                  # defined with some parameter like __call__(value), no we can directly call this __call__ method by object of the hello class and pass in the value for parameter like obj_hello(8).
                                                  # Watch this video if you want to understand about __call__ method more, https://www.youtube.com/watch?v=O6jOw80IRQQ
                                                  # Why we need the __call__ method here : Django wants middleware to behave like a function that takes a request and returns a response, but it also wants middleware to be an object that can
                                                  # store data (like get_response) created once. The __call__ method makes this possible. When Django calls the middleware object, Python automatically runs the __call__ method. Inside that method,
                                                  # your code runs before the view, then get_response(request) calls the view, and then your code runs after the view. Without __call__, Django would have no standard way to pass the request into
                                                  # the middleware and get a response back. UNDERSTAND WHY WE __call__ is used in more depth
                                                  
        
        print("This executes before view")        ## This line runs before the request reaches the view i.e. whatever is written before response = self.get_response(request), executes before the view. At this point You can read or modify request
                                                   # or You can even block the request and return a response early. At this time we have the request object and we also have the view in self.get_response(if its the last middleware), so here we 
                                                   # can play with request object like we can return it early, we can modify it e.g you want to render an html directly from here(imagine your main view is still under cosntruction) so here we can 
                                                   # do is:  return render(request, 'blog/under_construction.html'). Now with this this html will rendered directly to the client instead of the main view.
        
        response = self.get_response(request)     ## Imagine there is only one middleware, and it is the last middleware, so get_response points directly to the view that matches the URL i.e the view the URL maps to from URL.py. A request comes
                                                   # to Django, and Django creates a request object. This request object contains things like request type (GET/POST), user info, headers, etc. Django then calls your middleware object and passes
                                                   # this request to the __call__ method. 
                                                   # Inside __call__, when we write, response = self.get_response(request), what you are really doing is calling the view function, because get_response is pointing to that view. You pass the
                                                   # request object to the view, exactly the same way Django normally passes request to a view. The view uses that request data, runs its logic, and then returns an HttpResponse.
                                                   # That returned HttpResponse comes back to the middleware and is stored in the variable response. The middleware can now modify it if it wants, and then it returns that response to Django,
                                                   # which finally sends it back to the client.
        
        print("This executes after view")          # This line runs after the view has executed a response and then the response(below line) is sent to the client. This is the response phase. At this point: You can modify headers, Add cookies,
                                                   # Log response data and Change status codes
        
        return response
"""

## Actual code from below -- How we lead to this custom middleware, why we wrote this and why we have added custom header defined in this(response["X-Django-User"] = request.user.email) and what is custom header, all is defined below

###  Q1 -- What is the main requirement of all this?
###  A1 -- See as you know that we are logging with loguru and there is a requirement that for every response(from server) should contain an extra header which is basically the authenticated user's email. In simple words if an authenticated
###        user interacts with the server and does any type of request on a resource, the response should contain the email of the user who did that request AND THIS SHOULD FOR EVERY REQUEST ON ANY OF THE VIEW/URL. Now when we add extra
###        data/field to a response object(which is in form of dict), that is called custom header(defined below in detail)

###  Q2 -- What is a custom header and why it is used
###  A2 -- Custom headers in Django (like X-Django-User) are extra HTTP metadata added to a response to pass additional information to the client or to other services sitting in front of or behind your app (such as Nginx, API gateways, 
#          or frontend apps). They don’t affect the response body or business logic; instead, they travel with the HTTP response and are commonly used for debugging, tracing, authentication context, feature flags, or internal communication.
#          The X- prefix is just a convention, not a rule. Historically, it was used to mean “this is a non-standard, custom header”—something defined by your application, not part of the official HTTP spec. It is not mandatory. You can name headers  
#          without X-, e.g. Django-User or User-Email. IN VERY SIMPLE WORDS, IF YOU HAVE A RESPONSE OBJECT(like a get request of list of movies), YOU CAN ADD AN EXTRA FIELD IN THE RESPONSE OBJECT LIKE, 'X-Django-User' : 'mehranahmed22@gmail.com.
#          CUSTOM HEADERS ARE JUST EXTRA HEADER FIELDS THAT WE ADD ON YOUR RESPONSE OBJECT. In this case we want the email attached of authenticated user who is making the request to the server, so that whenever a response(obvious in dict format)
#          is returned, its returned with an extra custom field which specifies the email of the user who made that request for the response. Custom headers are mostly used for Logging & debugging → identify which user made a request (X-Django-User,
#          X-Request-ID), Tracing → track a request across multiple services in microservices etc. 

###  Q3 -- Why customer header used with middleware
###  A3 -- As I said above Custom headers are used to pass extra, structured information alongside an HTTP request or response without changing the actual data being sent, which makes them ideal for things like user context, request tracing,
#          versioning, or debugging. They are mostly implemented using middleware because middleware sits in a central place where it can intercept every request and response, ensuring the header is added consistently across all views without
#          repeating code. Middleware is perfect for this kind of cross-cutting concern since it runs automatically for all endpoints. In short as every request and response goes through middleware, its the best place to add a custom header,
#          so that the extra header is there in every response and we dont have to write repeated code



class CustomHeaderMiddleware:
    def __init__(self, get_response):
        
        self.get_response = get_response

    def __call__(self, request):
        
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            
            response["X-Django-User"] = request.user.email   ## Here we add the field "X-Django-User : user@email.com" to the response object that is being returned to the user/client. And we know from above explanation of custom middleware
                                                              # that anything after this line i.e. response = self.get_response(request) is after the request has been executed and response has been generated. So we know after this line
                                                              # response = self.get_response(request), we will always have a response object(in dict form obviously)
            
        return response