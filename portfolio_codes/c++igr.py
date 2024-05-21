class Face{
    /*
    represents a square face of a cube (could also represent a rectangle)
    */

public:
    Face(Vec3f sommet1, Vec3f sommet2, Vec3f sommet3, Vec3f normal, real size):
    sommet1(sommet1), sommet2(sommet2), sommet3(sommet3){
        e1 = sommet2-sommet1;
        e2 = sommet3-sommet1;
        initialized_mats = false;

        width = size;
        height = size;

    void initialize_mats(){
        initialized_mats = true;
        e1.normalize();
        e2.normalize();
        normal.normalize();
        matrice_passage_inv = Mat3f(e1, e2, normal);
        matrice_passage = Mat3f.inversed();
    }

    Vec3f get_coor_in_face_base(Vec3f& coor_euclide){
        if (!initialized_mats) initialize_mats;
        return matrice_passage*coor_euclide;
    }

    bool is_in_face(Vec3f& coor_face){
        return (coor_face[0]<width && coor_face[1]<height)

    real distance_inside_cube(Vec3f& coor_euclide){
        Vec3f coor_face = get_coor_in_face_base(coor_euclide);
        if (is_in_face()) return -coor_face[2];  // positive if point is inside cube (other sense than normal)
        return -1;  // not inside

private:
    
    real width, height;
    //Vec3f position;
    //Mat3f rotation;

    Vec3f sommet1, sommet2, sommet3;
    Vec3f e1, e2, normal;

    Mat3f matrice_passage;
    Mat3f matrice_passage_inv;

    bool initialized_mats;  // the matrice_passage are computed only if a fine grain collision test is necessary



## in box

bounding_sphere_radius = width*glm::sqrt(3)/2

std::vector<Face> local_faces{};
std::vector<Face> faces{};


real size = 0.5;

// faces starting from the bottom left far corner
// -1
Vec3f origine(-size, -size, -size);
Vec3f sommet_un(size, -size, -size);
Vec3f sommet_deux(-size, size, -size);
Vec3f normale(0, 0, 1);

local_faces.push_back(Face(origine, sommet_un, sommet_deux, normale, size));

//1
sommet_un(size, -size, -size);
sommet_deux(-size, -size, size);
normale(0, 1, 0);

local_faces.push_back(Face(origine, sommet_un, sommet_deux, normale, size));

// -1
sommet_un(-size, size, -size);
sommet_deux(-size, -size, size);
normale(1, 0, 0);

local_faces.push_back(Face(origine, sommet_un, sommet_deux, normale, size));

// faces starting from the upper rignt near corner
// 1
origine(size, size, size);
sommet_un(-size, size, size);
sommet_deux(size, -size, size);
normale(0, 0, 1);

local_faces.push_back(Face(origine, sommet_un, sommet_deux, normale, size));

// -1
sommet_un(-size, size, size);
sommet_deux(size, size, -size);
normale(0, 1, 0);

local_faces.push_back(Face(origine, sommet_un, sommet_deux, normale, size));

// 1
sommet_un(size, -size, size);
sommet_deux(size, size, -size);
normale(1, 0, 0);

local_faces.push_back(Face(origine, sommet_un, sommet_deux, normale, size));


void update_faces(){
    faces.clear();
    for (Face face:local_faces){
        Vec3f face_origin = local_to_world(face.sommet1);
        Vec3f face_sommet_e1 = local_to_world(face.sommet2);
        Vec3f face_sommet_e2 = local_to_world(face.sommet3);
        Vec3f face_normal = local_to_rotated_vect(face.normal);
        faces.push_back(Face(face_origin, face_sommet_e1, face_sommet_e2, face_normal, face.width));
    }
}


bool broad_test_collision(Box box2){
    /* can return false positives, but no false negatives */
    (X-box2.X).norm() <= bounding_sphere_radius+box2.bounding_sphere_radius;
}


std::vector<Contact> fine_grain_test_collision(Box box2){
    /* returns list of contacts:
    each contact stores a vertex-face collision between *this* and *box2*
    the vertex belongs to *this*, the face to *box2*
    */
    std::vector<Contact> all_contacts{};

    for (Vec3f sommet:get_world_vertex_positions()){
        bool all_inside = true;  // collision contact if the point is "inside" from the perspective of each face
        real min_dist = -1;  // we seach the closest face that
        int collision_face_idx = -1;
        int c = 0;
        for (Face face:faces){
            real dist = face.distance_inside_cube(sommet);
            if (dist >= 0){
                if (min_dist == -1 || dist < min_dist){  // new best face
                    min_dist = dist;
                    collision_face_idx = c;
                }
            else{
                // not collision point
                all_inside=false;
                break;
            }
            c ++;
        }

        if (all_inside){
            Contact n_contact(this, body2, sommet, faces[collision_face_idx].normal);
            all_contacts.push_back(n_contact);
        }
    }
}


## in Simulator


deal_with_collision(){
    for (int i=0; i<bodies.size(); i++){
        Box& body1 = bodies[i];
        for (int j=i+1; j<bodies.size(); j++){
            Box& body2 = bodies[i];
            if (body1.broad_test_collision(body2)){
                add_vect_to_vect(list_contacts, body1.fine_grain_test_collision(body2));
                add_vect_to_vect(list_contacts, body2.fine_grain_test_collision(body1));
            }
        }
    }


}
                













    
    
