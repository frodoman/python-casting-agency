from flask import Flask, render_template, request, abort, jsonify, session

# Add error handlers to the main app
def add_error_routes(app:Flask):

	@app.errorhandler(422)
	def error_unprocessable(error):
		return jsonify({
						"success": False,
						"error": 422,
						"message": "unprocessable"
						}), 422


	@app.errorhandler(404)
	def error_not_found(error):
		return jsonify({
		  "success": False,
		  "error": 404,
		  "message": "Not found!"
		}), 404


	@app.errorhandler(401)
	def error_unauthorized(error):
		return jsonify({
		  "success": False,
		  "error": 401,
		  "message": "Unauthorized!"
		}), 401

		
	@app.errorhandler(403)
	def error_not_permitted(error):
		return jsonify({
			"success": False,
			"error": 403,
			"message": "Not permitted!"
		}), 403


	@app.errorhandler(400)
	def error_bad_request(error):
		return jsonify({
		"success": False,
		"error": 400,
		"message": "Bad request!"
		}), 400


	@app.errorhandler(405)
	def error_not_allowed(error):
		return jsonify({
		"success": False,
		"error": 405,
		"message": "Method not allowed!"
		}), 405


	@app.errorhandler(500)
	def error_server(error):
		return jsonify({
		"success": False,
		"error": 500,
		"message": "Internal server error."
		}), 500

	# end of add_error_routes
	return 